# Task: Camera

**SDK Version:** iOS 27.1

## Overview

iPhone Duo has a front camera above each display. Opening or closing moves the app to the other display, so a camera that faced the user can now face away. This task keeps capture pointing the right way, fixes preview and rotation, and — only with decision Q11 — adds outer-display content during capture.

**The simulator has no camera.** Everything here must be checked on a physical iPhone Duo; say so in the report.

## Detection

| Finding | Rule id |
|---|---|
| `AVCaptureDevice.DiscoverySession`, `AVCaptureDevice.default(` | `camera-discovery` |
| `.position == .front` / `.back` used to decide mirroring or UI | `camera-position-logic` |
| `videoOrientation`, `videoRotationAngle`, manual rotation math | `camera-rotation` |
| `AVCaptureVideoPreviewLayer` | `camera-preview` |

## Patterns

### 1. Front camera that follows the display (simplest)
Existing front-camera discovery keeps working: on iPhone Duo `.builtInWideAngleCamera` / `.builtInUltraWideCamera` with position `.front` return a **virtual front camera** that switches automatically. Its capabilities are the common subset of both cameras. Use `isVirtualDevice` / `activePrimaryConstituent` to know which camera streams. **No change needed** unless the app needs features only one camera has.

### 2. Physical cameras + direction coordinator (camera-first apps)
```swift
import AVKit

@MainActor
final class DirectionObserver {
    private var coordinator: AVCaptureDeviceDirectionCoordinator?

    func start(previewView: UIView, onChange: @escaping (AVCaptureDeviceDirectionMap) -> Void) {
        coordinator = AVCaptureDeviceDirectionCoordinator(
            view: previewView,
            deviceTypes: [.builtInOuterUltraWideCamera, .builtInInnerUltraWideCamera, .builtInDualWideCamera]
        ) { map in onChange(map) }
    }
}
```
- List every built-in camera the app uses, including rear ones (a rear camera can face the user).
- The handler fires soon after creation and on every change, on the main actor. Keep the active camera if it's still in `forwardFacingDeviceDescriptors`; otherwise reconfigure the session with the first forward-facing one (pass the `AVCaptureDeviceDescriptor` to your capture actor).
- Mirror the preview based on **facing direction**, not `position`.
- Hold the coordinator as long as the preview is on screen; one coordinator per preview view.

### 3. Rotation and preview
- Use `AVCaptureDevice.RotationCoordinator` instead of manual orientation math.
- Choose `videoGravity` (`.resizeAspect` / `.resizeAspectFill`) per display shape; the inner display is near-square.

### 4. Outer-display content during capture (Q11 = yes)
```swift
CameraView(model: model)
    .sceneAccessory {
        CameraCaptureAccessory(isEnabled: $model.showsTeleprompter) {
            TeleprompterView(model: model)
        }
        .onAvailabilityChange { model.isTeleprompterAvailable = $0 }
    }
    .toolbar { TeleprompterToggle(isOn: $model.showsTeleprompter).disabled(!model.isTeleprompterAvailable) }
```
UIKit: `registerSceneAccessory(_:)` on the view controller showing the capture UI; the accessory scene's session role is `.windowCameraCaptureAccessory`.
Rules: accessory content is an enhancement — the app must work without it; keep essential controls in the main UI; share the same model object; give users a toggle rather than unregistering. Shown only while the device is open, the app is foreground, and capture is running.

## Implementation Gates

- No change when the virtual front camera already covers the app's needs.
- New APIs gated for iOS 27.1.
- Capture session reconfiguration stays on the capture actor/queue.

## Post-file Checklist

- [ ] Builds.
- [ ] Mirroring keyed to facing direction.

## Final Verification

Simulator: the capture UI lays out correctly on both displays (camera feed will be absent). Report a physical-device checklist: open/close while previewing; selfie with rear camera when folded closed; rotation; accessory appears/disappears with fold and capture state.

## API Reference

See `api-facts.md` → Camera, Scenes & accessories.
