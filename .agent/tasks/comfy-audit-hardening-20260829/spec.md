# comfy-audit-hardening-20260829 Spec

## Task

Finish and independently re-verify the ComfyUI Colab pack hardening requested by the user after the sampling audit.

## Acceptance Criteria

- AC1. Every bundled workflow folder contains exactly one `workflow.json`; multi-model notebooks may place multiple model branches on that one canvas, with no runtime-generated workflow zoo.
- AC2. Every active model branch except FLUX.2 Klein 9B and Qwen-Image-Edit-2511 has main generation -> refiner -> FaceDetailer -> HandDetailer, with refiner/detailer steps, CFG/guidance semantics, sampler, and scheduler matching the model's main sampling; only denoise is intentionally reduced (refiner 0.30, face 0.50, hand 0.35).
- AC3. FLUX.2 Klein 9B has no refiner/detailers and keeps Base 50/CFG4/Euler plus Distilled 4/CFG1/Euler on one bundled canvas. Qwen-Image-Edit-2511 has no refiner/detailers and uses mandatory 8-step Lightning at 8/CFG1/Euler/simple.
- AC4. Qwen-Image-2512 uses mandatory Qwen-Image-2512 8-step Lightning at 8/CFG1/Euler/simple, including its refiner/detailers.
- AC5. Every bundled model branch ends with optional SeedVR2 before its output/save path, bypassed by default, using the registered 3B Q4_K_M low-VRAM profile (32 block swap, CPU offload, tiled VAE, batch 1).
- AC6. Every notebook (active, universal, and paused) uses the unified ComfyUI+tunnel watchdog with Manager-safe restart grace; model notebooks with detailers install Face/Hand YOLO plus SAM, and their workflow SAMLoader is CPU mode.
- AC7. All workflow links are structurally valid; Face/Hand use the intended model/CLIP/VAE/conditioning/detectors; custom-sampler models preserve their native guidance/sigma schedule semantics.
- AC8. Helper scripts cannot reintroduce old behavior: notebook/workflow validators enforce the new architecture, bundled installer uses current Qwen 8-step names and one-flow Klein behavior, and shared runtime fixer knows the unified dependencies.
- AC9. Sampling audit fixes remain applied: RouWei 28/5/EulerA/normal, Z-Image Base 30/4/res_multistep/simple, Chroma exact 26/3.8/Euler/Beta(0.45,0.45)/shift1, SRPO 50/FluxGuidance3.5/Euler/normal.
- AC10. Final proof record has no open problems: every criterion is PASS and the proof document validates against proof-loop-lite rules.

## Constraints

- Push directly to `main`.
- Keep one bundled workflow file per workflow folder.
- Do not add refiner/detailers to FLUX.2 Klein 9B or Qwen-Image-Edit-2511.
- SeedVR2 remains bypassed by default to avoid unexpected VRAM cost.
- ComfyUI watchdog must not race ComfyUI-Manager restarts.

## Non-Goals

- Runtime image-quality benchmarking on an actual Colab T4 in this session.
- Reactivating paused model notebooks or adding new bundled workflows for them.

## Verification

- Repository-wide static workflow topology and link audit.
- Notebook watchdog/dependency audit and Python-cell syntax validator.
- Model-specific sampling parity assertions.
- Helper-script regression assertions.
- proof-loop-lite proof.json schema/verdict validation.
