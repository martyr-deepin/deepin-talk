import QtQuick 2.1
import QtGraphicalEffects 1.0

Rectangle {
	id: container
	property string source
    color: Qt.rgba(0, 0, 0, 0)
	
	Canvas {
		id: canvas
		renderTarget: Canvas.Image 		
		anchors.fill: parent
		property int offset: 1
		property rect drawRect: Qt.rect(x+offset, y+offset, width-offset*2, height-offset*2)		
		
		Component.onCompleted: {
			loadImage(container.source)
		}
        onWidthChanged:  requestPaint()
        onHeightChanged: requestPaint()
		onImageLoaded: {
			requestPaint()
		}
		
		onPaint: {
			var ctx = canvas.getContext("2d")
			ctx.save()
			ctx.ellipse(drawRect.x, drawRect.y, drawRect.width, drawRect.height)
			ctx.clip()
			if (isImageLoaded(container.source)) {
				ctx.drawImage(container.source, drawRect.x, drawRect.y, drawRect.width, drawRect.height)
			} 
			ctx.restore()
		}
	}
}
