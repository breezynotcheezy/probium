from __future__ import annotations

from ..scoring import score_magic, score_tokens
from ..models import Candidate, Result
from .base import EngineBase
from ..registry import register

_SHEBANGS = [b"#!/bin/sh", b"#!/bin/bash", b"#!/usr/bin/env bash", b"#!/usr/bin/env sh"]

@register
class SHEngine(EngineBase):
    name = "sh"
    cost = 0.05

    def sniff(self, payload: bytes) -> Result:
        for magic in _SHEBANGS:
            if payload.startswith(magic):
                cand = Candidate(
                    media_type="application/x-sh",
                    extension="sh",
                    confidence=score_tokens(1.0),
                    breakdown={"token_ratio": 1.0},
                )
                return Result(candidates=[cand])
        return Result(candidates=[])
