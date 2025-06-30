from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import time
import hashlib
import os
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime

# Import the actual Probium library
import probium
from probium.core import detect, scan_dir, _detect_file
from probium.registry import list_engines, get_instance
from probium.models import Result, Candidate

app = FastAPI(title="Probium API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state for tracking scans and system metrics
active_scans = {}
scan_history = []
system_metrics = {
    "cpu_usage": 0.0,
    "memory_usage": 0.0,
    "active_threads": 0,
    "total_scans": 0,
    "engine_stats": {}
}

def calculate_file_hashes(file_path: Path) -> Dict[str, str]:
    """Calculate MD5, SHA1, SHA256, and CRC32 hashes for a file."""
    hashes = {}
    
    with open(file_path, 'rb') as f:
        content = f.read()
        
    # MD5
    hashes['md5'] = hashlib.md5(content).hexdigest()
    
    # SHA1
    hashes['sha1'] = hashlib.sha1(content).hexdigest()
    
    # SHA256
    hashes['sha256'] = hashlib.sha256(content).hexdigest()
    
    # CRC32
    import zlib
    hashes['crc32'] = format(zlib.crc32(content) & 0xffffffff, '08x')
    
    return hashes

def extract_metadata(file_path: Path, result: Result) -> Dict[str, Any]:
    """Extract metadata from the file based on its detected type."""
    metadata = {
        "filename": file_path.name,
        "size": file_path.stat().st_size,
        "created": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
    }
    
    # Add type-specific metadata based on detection result
    if result.candidates:
        candidate = result.candidates[0]
        if candidate.media_type.startswith("application/pdf"):
            # PDF-specific metadata would go here
            metadata.update({
                "pages": None,  # Would need PyPDF2 or similar
                "encrypted": False,
                "version": None,
            })
        elif candidate.media_type.startswith("image/"):
            # Image-specific metadata would go here
            metadata.update({
                "width": None,
                "height": None,
                "color_depth": None,
            })
    
    return metadata

def analyze_file_structure(file_path: Path, result: Result) -> Dict[str, Any]:
    """Analyze file structure based on detected type."""
    structure = {
        "valid": True,
        "corrupted": False,
        "suspicious": False,
    }
    
    if result.candidates:
        candidate = result.candidates[0]
        # Add structure analysis based on file type
        if candidate.media_type.startswith("application/pdf"):
            structure.update({
                "objects": None,
                "streams": None,
                "xref_entries": None,
                "linearized": False,
            })
    
    return structure

def assess_security(file_path: Path, result: Result) -> Dict[str, Any]:
    """Perform security assessment of the file."""
    security = {
        "malware_score": 0.0,
        "threat_level": "low",
        "signatures": [],
        "anomalies": [],
        "embedded": {
            "files": 0,
            "scripts": 0,
            "forms": 0,
        }
    }
    
    # Basic security checks
    file_size = file_path.stat().st_size
    
    # Flag very large files as potentially suspicious
    if file_size > 100 * 1024 * 1024:  # 100MB
        security["anomalies"].append("Large file size")
        security["malware_score"] += 0.1
    
    # Check for suspicious extensions vs detected type mismatch
    if result.candidates:
        candidate = result.candidates[0]
        expected_ext = candidate.extension
        actual_ext = file_path.suffix.lower().lstrip('.')
        
        if expected_ext and actual_ext and expected_ext != actual_ext:
            security["anomalies"].append("Extension mismatch")
            security["malware_score"] += 0.2
    
    # Determine threat level
    if security["malware_score"] >= 0.7:
        security["threat_level"] = "high"
    elif security["malware_score"] >= 0.3:
        security["threat_level"] = "medium"
    
    return security

@app.get("/api/v1/engines")
async def get_engines():
    """Get list of all available Probium engines."""
    try:
        engines = list_engines()
        engine_details = []
        
        for engine_name in engines:
            try:
                engine_instance = get_instance(engine_name)
                engine_details.append({
                    "name": engine_name,
                    "cost": getattr(engine_instance, 'cost', 0.1),
                    "status": "active",
                    "version": "1.0.0",  # Would need to get from engine if available
                })
            except Exception as e:
                logger.warning(f"Failed to get details for engine {engine_name}: {e}")
                engine_details.append({
                    "name": engine_name,
                    "cost": 0.1,
                    "status": "error",
                    "version": "unknown",
                })
        
        return {
            "success": True,
            "engines": engine_details,
            "total": len(engine_details)
        }
    except Exception as e:
        logger.error(f"Failed to get engines: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/engines/status")
async def get_engine_status():
    """Get status and performance metrics for all engines."""
    try:
        engines = list_engines()
        engine_status = {}
        
        for engine_name in engines:
            # Get stats from global metrics or calculate
            stats = system_metrics["engine_stats"].get(engine_name, {
                "scans_completed": 0,
                "avg_time": 0.0,
                "last_used": None,
                "performance": 95.0,  # Default performance score
            })
            
            engine_status[engine_name] = {
                "status": "active",
                "performance": stats["performance"],
                "scans_completed": stats["scans_completed"],
                "avg_time": stats["avg_time"],
                "last_used": stats["last_used"],
            }
        
        return {
            "success": True,
            "engines": engine_status
        }
    except Exception as e:
        logger.error(f"Failed to get engine status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/scan/file")
async def scan_file(
    file: UploadFile = File(...),
    engines: Optional[str] = None,
    deep_analysis: bool = True,
    generate_hashes: bool = True,
    extract_metadata: bool = True,
    validate_signatures: bool = True,
):
    """Scan a single file using Probium engines."""
    scan_start_time = time.time()
    scan_id = f"scan_{int(scan_start_time * 1000)}"
    
    try:
        # Update active scans
        active_scans[scan_id] = {
            "filename": file.filename,
            "status": "scanning",
            "progress": 0,
            "start_time": scan_start_time,
        }
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = Path(tmp_file.name)
        
        try:
            # Parse engines parameter
            engine_list = None
            if engines:
                engine_list = [e.strip() for e in engines.split(',')]
            
            # Update progress
            active_scans[scan_id]["progress"] = 20
            active_scans[scan_id]["current_stage"] = "Initializing engines"
            
            # Perform detection using actual Probium
            detection_start = time.time()
            
            if engine_list:
                result = _detect_file(tmp_file_path, only=engine_list)
            else:
                result = _detect_file(tmp_file_path)
            
            detection_time = time.time() - detection_start
            
            # Update progress
            active_scans[scan_id]["progress"] = 60
            active_scans[scan_id]["current_stage"] = "Analyzing file structure"
            
            # Generate comprehensive result
            scan_result = {
                "id": scan_id,
                "filename": file.filename,
                "size": len(content),
                "detected_type": result.candidates[0].media_type if result.candidates else "unknown",
                "mime_type": result.candidates[0].media_type if result.candidates else "application/octet-stream",
                "confidence": result.candidates[0].confidence if result.candidates else 0.0,
                "extension": result.candidates[0].extension if result.candidates else None,
                "engines_used": engine_list or list_engines(),
                "scan_time": f"{detection_time:.3f}s",
                "timestamp": datetime.now().isoformat(),
                "probium_version": probium.__version__,
            }
            
            # Add breakdown information if available
            if result.candidates and result.candidates[0].breakdown:
                scan_result["breakdown"] = result.candidates[0].breakdown
            
            # Generate hashes if requested
            if generate_hashes:
                active_scans[scan_id]["progress"] = 75
                active_scans[scan_id]["current_stage"] = "Generating hashes"
                scan_result["hashes"] = calculate_file_hashes(tmp_file_path)
            
            # Extract metadata if requested
            if extract_metadata:
                active_scans[scan_id]["progress"] = 85
                active_scans[scan_id]["current_stage"] = "Extracting metadata"
                scan_result["metadata"] = extract_metadata(tmp_file_path, result)
            
            # Analyze structure if deep analysis is enabled
            if deep_analysis:
                active_scans[scan_id]["progress"] = 90
                active_scans[scan_id]["current_stage"] = "Analyzing structure"
                scan_result["structure"] = analyze_file_structure(tmp_file_path, result)
            
            # Perform security assessment
            active_scans[scan_id]["progress"] = 95
            active_scans[scan_id]["current_stage"] = "Security assessment"
            scan_result["security"] = assess_security(tmp_file_path, result)
            
            # Calculate performance metrics
            total_scan_time = time.time() - scan_start_time
            scan_result["performance"] = {
                "total_time": f"{total_scan_time:.3f}s",
                "detection_time": f"{detection_time:.3f}s",
                "memory_used": f"{len(content) / 1024 / 1024:.2f}MB",
                "cpu_time": f"{detection_time:.3f}s",
                "efficiency": f"{len(content) / 1024 / 1024 / total_scan_time:.1f} MB/s"
            }
            
            # Update progress
            active_scans[scan_id]["progress"] = 100
            active_scans[scan_id]["current_stage"] = "Complete"
            active_scans[scan_id]["status"] = "complete"
            
            # Update global metrics
            system_metrics["total_scans"] += 1
            for engine in scan_result["engines_used"]:
                if engine not in system_metrics["engine_stats"]:
                    system_metrics["engine_stats"][engine] = {
                        "scans_completed": 0,
                        "total_time": 0.0,
                        "avg_time": 0.0,
                        "last_used": None,
                        "performance": 95.0,
                    }
                
                stats = system_metrics["engine_stats"][engine]
                stats["scans_completed"] += 1
                stats["total_time"] += detection_time
                stats["avg_time"] = stats["total_time"] / stats["scans_completed"]
                stats["last_used"] = datetime.now().isoformat()
            
            # Add to scan history
            scan_history.append(scan_result)
            
            # Clean up active scan
            del active_scans[scan_id]
            
            return {
                "success": True,
                "result": scan_result
            }
            
        finally:
            # Clean up temporary file
            try:
                tmp_file_path.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete temporary file: {e}")
                
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        if scan_id in active_scans:
            active_scans[scan_id]["status"] = "error"
            active_scans[scan_id]["error"] = str(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/scan/batch")
async def scan_batch(
    files: List[UploadFile] = File(...),
    engines: Optional[str] = None,
    parallel_processing: bool = True,
    thread_pool_size: int = 8,
):
    """Scan multiple files in parallel."""
    batch_id = f"batch_{int(time.time() * 1000)}"
    batch_start_time = time.time()
    
    try:
        results = []
        engine_list = None
        if engines:
            engine_list = [e.strip() for e in engines.split(',')]
        
        # Process files
        for i, file in enumerate(files):
            try:
                # Save file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp_file:
                    content = await file.read()
                    tmp_file.write(content)
                    tmp_file_path = Path(tmp_file.name)
                
                try:
                    # Detect file type
                    detection_start = time.time()
                    if engine_list:
                        result = _detect_file(tmp_file_path, only=engine_list)
                    else:
                        result = _detect_file(tmp_file_path)
                    detection_time = time.time() - detection_start
                    
                    # Create result
                    file_result = {
                        "filename": file.filename,
                        "size": len(content),
                        "detected_type": result.candidates[0].media_type if result.candidates else "unknown",
                        "confidence": result.candidates[0].confidence if result.candidates else 0.0,
                        "extension": result.candidates[0].extension if result.candidates else None,
                        "scan_time": f"{detection_time:.3f}s",
                        "index": i,
                    }
                    
                    results.append(file_result)
                    
                finally:
                    # Clean up temporary file
                    try:
                        tmp_file_path.unlink()
                    except Exception as e:
                        logger.warning(f"Failed to delete temporary file: {e}")
                        
            except Exception as e:
                logger.error(f"Failed to process file {file.filename}: {e}")
                results.append({
                    "filename": file.filename,
                    "error": str(e),
                    "index": i,
                })
        
        total_time = time.time() - batch_start_time
        
        return {
            "success": True,
            "batch_id": batch_id,
            "total_files": len(files),
            "completed": len([r for r in results if "error" not in r]),
            "failed": len([r for r in results if "error" in r]),
            "results": results,
            "total_time": f"{total_time:.3f}s",
            "timestamp": datetime.now().isoformat(),
        }
        
    except Exception as e:
        logger.error(f"Batch scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/scan/{scan_id}/status")
async def get_scan_status(scan_id: str):
    """Get the status of an active scan."""
    if scan_id in active_scans:
        return {
            "success": True,
            "scan": active_scans[scan_id]
        }
    else:
        # Check if it's in history
        for scan in scan_history:
            if scan["id"] == scan_id:
                return {
                    "success": True,
                    "scan": {
                        "status": "complete",
                        "progress": 100,
                        "result": scan
                    }
                }
        
        raise HTTPException(status_code=404, detail="Scan not found")

@app.get("/api/v1/system/metrics")
async def get_system_metrics():
    """Get current system metrics and statistics."""
    import psutil
    
    # Get real system metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Update global metrics
    system_metrics.update({
        "cpu_usage": cpu_percent,
        "memory_usage": memory.percent,
        "memory_total": memory.total,
        "memory_used": memory.used,
        "disk_usage": disk.percent,
        "disk_total": disk.total,
        "disk_used": disk.used,
        "active_threads": len(active_scans),
        "timestamp": datetime.now().isoformat(),
    })
    
    return {
        "success": True,
        "metrics": system_metrics
    }

@app.get("/api/v1/scan/history")
async def get_scan_history(limit: int = 100):
    """Get recent scan history."""
    return {
        "success": True,
        "scans": scan_history[-limit:],
        "total": len(scan_history)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
