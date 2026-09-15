# Dock dismissal — physical phone, 2026-09-14

Removed Return and Theme Configuration by replacing their seven children with one transparent background touch region. Reused original Return actions: detail=0, view=0, parent=0. The root group stayed below the terminal interaction group, retaining terminal button touch priority.

Kept the existing page-change flow. Added a wallpaper-visibility-change flow that directly stores 0 into view. Rechecking visibility inside the action missed app returns; the final unconditional reset on visibility change passed. Native flow count remains two.

Verified on the connected Xiaomi HyperOS phone:

- Header controls removed: final-before-swipe.png.
- Top and left blank-area taps close terminal; sidebar and diagonal bar return: final-outside-tap.png and 02-outside-tap.png.
- Desktop page change and return leave terminal closed: final-page-return.png.
- Terminal WeChat button directly launches com.tencent.mm/.ui.LauncherUI; no chat contents inspected or messages sent.
- Returning from WeChat leaves terminal closed: final-app-return.png.
- Phone left on ordinary theme page with terminal closed.

This validates blank wallpaper taps, desktop page changes, and app leave/return, not every HyperOS overlay or system gesture.
