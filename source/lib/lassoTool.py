from mojo.events import EditingTool, installTool
from mojo.extensions import ExtensionBundle
from mojo.UI import getDefault, appearanceColorKey
import AppKit


bundle = ExtensionBundle("Lasso Tool")
toolbarIcon = bundle.get("LassoToolIcon")
_cursor = AppKit.NSCursor.crosshairCursor()


class LassoTool(EditingTool):

    def setup(self):
        container = self.extensionContainer(
            identifier="LassoTool.foreground",
            location='foreground',
            clear=True
        )

        self.selectionFillColor = getDefault(appearanceColorKey("glyphViewSelectionMarqueColor"))
        r, g, b, a = self.selectionFillColor
        self.selectionStrokeColor = (r, g, b, 1)

        self.selectionContourLayer = container.appendPathSublayer(
            fillColor=self.selectionFillColor,
            strokeColor=self.selectionStrokeColor,
            strokeWidth=1
        )

    def mouseDown(self, point, clickCount):
        self.pen = None
        # from RF4.6+
        # if self.mouseDownInSelection():
        if self._pointInSelection:
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
            for point in contour.points:
                result = containsPoint((point.x, point.y))
                if result:
                    point.selected = True
                elif not self.shiftDown:
                    point.selected = False

        self.selectionContourLayer.setPath(None)

    def canSelectWithMarquee(self):
        return False

    # deprecated in RF4.6
    canSelectWithMarque = canSelectWithMarquee

    def dragSelection(self, point, delta):
        # From RF4.6+
        # if self.mouseDownInSelection():
        if self._pointInSelection:
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
