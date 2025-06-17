from __future__ import annotations

from ..types import Candidate, Result
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
                cand = Candidate(media_type="application/x-sh", extension="sh", confidence=0.95)
                return Result(candidates=[cand])
        return Result(candidates=[])
