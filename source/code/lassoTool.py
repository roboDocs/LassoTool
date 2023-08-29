from mojo.events import EditingTool, installTool
from mojo.extensions import ExtensionBundle
from mojo.UI import getDefault, appearanceColorKey


bundle = ExtensionBundle("LassoTool")
toolbarIcon = bundle.get("LassoToolIcon")


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
        if self.selection.hasSelection():
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
                if self.shiftDown:
                    point.selected = not result
                else:
                    point.selected = result
        
        self.selectionContourLayer.setPath(None)
        
    def canSelectWithMarque(self):
        return False
    
    def getToolbarTip(self):
        return "lasso"
        
    def getToolbarIcon(self):
        return toolbarIcon


if __name__ == '__main__':
    lassoTool = LassoTool()
    installTool(lassoTool)