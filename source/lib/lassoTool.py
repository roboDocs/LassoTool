from mojo.events import EditingTool, installTool
from mojo.extensions import ExtensionBundle
from mojo.UI import getDefault, appearanceColorKey
import mojo
import AppKit


bundle = ExtensionBundle("Lasso Tool")
toolbarIcon = bundle.get("LassoToolIcon")
_cursor = AppKit.NSCursor.crosshairCursor()


class LassoTool(EditingTool):

    version = float(mojo.roboFont.version.replace('b', ''))

    def setup(self):
        container = self.extensionContainer(
            identifier="LassoTool.foreground",
            location='foreground',
            clear=True
        )

        if self.version < 4.6:
            self.selectionFillColor = getDefault(appearanceColorKey(
                "glyphViewSelectionMarqueColor"))
        else:
            self.selectionFillColor = getDefault(appearanceColorKey(
                "glyphViewSelectionMarqueeColor"))
        r, g, b, a = self.selectionFillColor
        self.selectionStrokeColor = (r, g, b, 1)

        self.selectionContourLayer = container.appendPathSublayer(
            fillColor=self.selectionFillColor,
            strokeColor=self.selectionStrokeColor,
            strokeWidth=1
        )

    def mouseDown(self, point, clickCount):
        self.pen = None
        if self.version < 4.6:
            if self._pointInSelection:
                return
        else:
            if self.mouseDownInSelection():
                return

        self.pen = self.selectionContourLayer.getPen(clear=True)
        self.pen.moveTo((point.x, point.y))
        self.pen.endPath()

    def mouseDragged(self, point, delta):
        if self.pen is not None:
            self.pen.lineTo((point.x, point.y))
            self.pen.endPath()

    def mouseUp(self, point):
        if self.pen is None:
            return
        glyph = self.getGlyph()
        containsPoint = self.selectionContourLayer.containsPoint

        for contour in glyph:
            offcurves = [p for p in contour.points if p.type == 'offcurve']
            oncurves = [p for p in contour.points if p not in offcurves]
            # only select offcurves when option is down
            if self.optionDown:
                for point in offcurves:
                    result = containsPoint((point.x, point.y))
                    if result:
                        point.selected = True
                    elif not self.shiftDown:
                        point.selected = False

            # only select oncurves otherwise
            # (this is analog to the default selection marquee)
            else:
                for point in oncurves:
                    result = containsPoint((point.x, point.y))
                    if result:
                        point.selected = True
                    elif not self.shiftDown:
                        point.selected = False

        self.selectionContourLayer.setPath(None)

    def canSelectWithMarque(self):
        # < 4.6
        return False

    def canSelectWithMarquee(self):
        # > 4.6
        return False

    def dragSelection(self, point, delta):
        if self.version < 4.6:
            if self._pointInSelection:
                super().dragSelection(point, delta)
        else:
            if self.mouseDownInSelection():
                super().dragSelection(point, delta)

    def getToolbarTip(self):
        return "Lasso Tool"

    def getToolbarIcon(self):
        return toolbarIcon

    def getDefaultCursor(self):
        return _cursor


if __name__ == '__main__':
    lassoTool = LassoTool()
    installTool(lassoTool)
