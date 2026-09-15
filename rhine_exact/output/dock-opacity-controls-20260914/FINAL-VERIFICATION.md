# Physical phone verification — 2026-09-14

Device: connected Xiaomi HyperOS phone, native launcher, official Huawei KLWP build.

## Final applied state

- KLWP Advanced > Disable Parallel Rendering enabled.
- Four temporary opacity diagnostic modules removed; formal theme saved.
- Following final save, KLWP was force-stopped and its live wallpaper re-applied to the home screen only.
- Original theme colors and animation tracks retained. Earlier resident visual-layer fix and native WeChat launch fix preserved.
- Phone left on theme page 2 with terminal open and normal paper opacity.

## Observations

- Static diagnostic white rendered correctly before restart; animated opacity controls and terminal were too transparent in wallpaper runtime.
- Disabling parallel rendering and restarting the wallpaper restored proper opaque animation endpoints and paper faces.
- Removing diagnostics and saving in the editor reproduced excessive transparency. A second restart after this final save restored correct rendering again.
- Root cause inside KLWP is not confirmed. This is a verified runtime workaround, not proof that later editor saves are permanently fixed.

## Final validation

- Three alternating round trips between page 2 and its neighboring pages: all terminal rows complete after opening, stable opacity. Evidence: final-1/2/3-returned.png and final-1/2/3-opened.png.
- WeChat button launched com.tencent.mm/.ui.LauncherUI directly. Only foreground activity identity inspected.
- Returning home retained all rows and normal opacity: final-app-return.png.
- No diagnostic rectangles remain visible.

If a later editor save reproduces the issue, restart and re-apply the saved KLWP home wallpaper. Do not restore an old autosave: it may revert page visibility and native WeChat fixes.
