import QtQuick 2.1
import QtGraphicalEffects 1.0

Rectangle {
    id: rect
    default property alias content: container.children    
    
    width: 200
    height: 200
    color: Qt.rgba(0, 0, 0, 0)

    property int borderMargin: 5    
    property bool withBlur: true
    property color fillColor: Qt.rgba(0, 0, 0, 0.7)
    property color blurColor: Qt.rgba(0, 0, 0, 1)
    property color borderColor: Qt.rgba(1, 1, 1, 0.15)

    property int blurWidth: 2
    property int borderWidth: 2
    property int rectRadius: 10
    property rect contentRect
    property bool isHalf: true
    property real widthMargin: adjustWidthMargin()
    property real heightMargin: adjustHeightMargin()

    property var cornerDirection: Qt.LeftEdge
    property string shadowDirection: "left"
    property int cornerPos: 20
    property int cornerWidth: 8
    property int cornerHeight: 10
    property alias painter: canvas
	onCornerDirectionChanged: canvas.requestPaint()
    onWidthChanged: canvas.requestPaint()
    onHeightChanged: canvas.requestPaint()
    onVisibleChanged: canvas.requestPaint()
    
    function adjustHeightMargin() {
        var tempHeight = blurWidth * 2 + borderMargin  * 2 
        if (cornerDirection == Qt.BottomEdge || cornerDirection == Qt.TopEdge ) {
            return tempHeight + cornerHeight 
        } else {
            return  tempHeight
        }
    }
    
    function adjustWidthMargin() {
        var tempWidth = blurWidth * 2 + borderMargin  * 2 
        if (cornerDirection == Qt.LeftEdge || cornerDirection == Qt.RightEdge ) {
            return tempWidth + cornerHeight 
        } else {
            return  tempWidth
        }
    }

    Canvas {
        id: canvas
        width: rect.width
        height: rect.height
        
        onPaint: {
            var ctx = getContext("2d")

            ctx.save()
            ctx.clearRect(0, 0, canvas.width, canvas.height)

            ctx.beginPath();

            if (cornerDirection == Qt.BottomEdge) {
                var x = blurWidth
                var y = blurWidth
                var w = rect.width - 2 * blurWidth
                var h = rect.height - 2 * blurWidth - cornerHeight
                
                rect.contentRect = Qt.rect(x, y, w, h)
                ctx.moveTo(x + rectRadius, y);                 // top side
                ctx.lineTo(x + w - rectRadius, y);
                // draw top right corner
                ctx.arcTo(x + w, y, x + w, y + rectRadius, rectRadius);
                ctx.lineTo(x+w,y+h-rectRadius);    // right side
                // draw bottom right corner
                ctx.arcTo(x+w,y+h,x+w-rectRadius,y+h,rectRadius);

                if (cornerPos < x + rectRadius + cornerWidth / 2) {
                    cornerPos = x + rectRadius + cornerWidth / 2
                }
                if (cornerPos > x + w - rectRadius - cornerWidth / 2) {
                    cornerPos = x + w - rectRadius - cornerWidth / 2
                }
                ctx.lineTo(cornerPos + cornerWidth / 2, y + h) /* corner */
                ctx.lineTo(cornerPos, y + h + cornerHeight)
                ctx.lineTo(cornerPos - cornerWidth / 2, y + h)

                ctx.lineTo(x+rectRadius,y+h);              // bottom side
                // draw bottom left corner
                ctx.arcTo(x,y+h,x,y+h-rectRadius,rectRadius);
                ctx.lineTo(x,y+rectRadius);                 // left side
                // draw top left corner
                ctx.arcTo(x,y,x+rectRadius,y,rectRadius);
                
            } else if (cornerDirection == Qt.TopEdge) {
                var x = blurWidth
                var y = blurWidth + cornerHeight
                var w = rect.width - 2 * blurWidth
                var h = rect.height - 2 * blurWidth - cornerHeight
                rect.contentRect = Qt.rect(x, y, w, h)

                ctx.moveTo(x + rectRadius, y);                 // top side

                if (cornerPos < x + rectRadius + cornerWidth / 2) {
                    cornerPos = x + rectRadius + cornerWidth / 2
                }
                if (cornerPos > x + w - rectRadius - cornerWidth / 2) {
                    cornerPos = x + w - rectRadius - cornerWidth / 2
                }
                ctx.lineTo(cornerPos - cornerWidth / 2, y) /* corner */
                ctx.lineTo(cornerPos, y - cornerHeight)
                ctx.lineTo(cornerPos + cornerWidth / 2, y)

                ctx.lineTo(x + w - rectRadius, y);

                // draw top right corner
                ctx.arcTo(x + w, y, x + w, y + rectRadius, rectRadius);
                ctx.lineTo(x+w,y+h-rectRadius);    // right side
                // draw bottom right corner
                ctx.arcTo(x+w,y+h,x+w-rectRadius,y+h,rectRadius);

                ctx.lineTo(x+rectRadius,y+h);              // bottom side
                // draw bottom left corner
                ctx.arcTo(x,y+h,x,y+h-rectRadius,rectRadius);
                ctx.lineTo(x,y+rectRadius);                 // left side
                // draw top left corner
                ctx.arcTo(x,y,x+rectRadius,y,rectRadius);
            } else if (cornerDirection == Qt.LeftEdge) {
                var x = blurWidth + cornerHeight
                var y = blurWidth
                var w = rect.width - 2 * blurWidth - cornerHeight
                var h = rect.height - 2 * blurWidth
                rect.contentRect = Qt.rect(x, y, w, h)

                ctx.moveTo(x + rectRadius, y);                 // top side
                ctx.lineTo(x + w - rectRadius, y);

                // draw top right corner
                ctx.arcTo(x + w, y, x + w, y + rectRadius, rectRadius);
                ctx.lineTo(x+w,y+h-rectRadius);    // right side
                // draw bottom right corner
                ctx.arcTo(x+w,y+h,x+w-rectRadius,y+h,rectRadius);

                ctx.lineTo(x+rectRadius,y+h);              // bottom side
                // draw bottom left corner
                ctx.arcTo(x,y+h,x,y+h-rectRadius,rectRadius);

                if (cornerPos < y + rectRadius + cornerWidth / 2) {
                    cornerPos = y + rectRadius + cornerWidth / 2
                }
                if (cornerPos > y + h - rectRadius - cornerWidth / 2) {
                    cornerPos = y + h - rectRadius - cornerWidth / 2
                }
                ctx.lineTo(x, cornerPos + cornerWidth / 2) /* corner */
                if (isHalf) {
                    ctx.lineTo(x - cornerHeight, cornerPos - cornerWidth / 2)
                    
                } else {
                    ctx.lineTo(x - cornerHeight, cornerPos)
                }
                
                
                ctx.lineTo(x, cornerPos - cornerWidth / 2)

                ctx.lineTo(x,y+rectRadius);                 // left side
                // draw top left corner
                ctx.arcTo(x,y,x+rectRadius,y,rectRadius);
            } else if (cornerDirection == Qt.RightEdge) {
                var x = blurWidth
                var y = blurWidth
                var w = rect.width - 2 * blurWidth - cornerHeight
                var h = rect.height - 2 * blurWidth
                rect.contentRect = Qt.rect(x, y, w, h)

                ctx.moveTo(x + rectRadius, y);                 // top side
                ctx.lineTo(x + w - rectRadius, y);

                // draw top right corner
                ctx.arcTo(x + w, y, x + w, y + rectRadius, rectRadius);

                if (cornerPos < y + rectRadius + cornerWidth / 2) {
                    cornerPos = y + rectRadius + cornerWidth / 2
                }
                if (cornerPos > y + h - rectRadius - cornerWidth / 2) {
                    cornerPos = y + h - rectRadius - cornerWidth / 2
                }
                ctx.lineTo(x + w, cornerPos - cornerWidth / 2) /* corner */
                if (isHalf) {
                    ctx.lineTo(x + w + cornerHeight, cornerPos - cornerWidth / 2)
                    
                } else {
                    ctx.lineTo(x + w + cornerHeight, cornerPos)
                }
                ctx.lineTo(x + w, cornerPos + cornerWidth / 2)
                

                ctx.lineTo(x+w,y+h-rectRadius);    // right side
                // draw bottom right corner
                ctx.arcTo(x+w,y+h,x+w-rectRadius,y+h,rectRadius);

                ctx.lineTo(x+rectRadius,y+h);              // bottom side
                // draw bottom left corner
                ctx.arcTo(x,y+h,x,y+h-rectRadius,rectRadius);

                ctx.lineTo(x,y+rectRadius);                 // left side
                // draw top left corner
                ctx.arcTo(x,y,x+rectRadius,y,rectRadius);
            }

            ctx.closePath();
            /* ctx.lineWidth = borderWidth */
            /* ctx.strokeStyle = borderColor */
            /* ctx.stroke() */

            /* var gradient = ctx.createLinearGradient(rect.width / 2, 0, rect.width / 2, rect.height); */
            /* gradient.addColorStop(0.0, Qt.rgba(0, 0, 0, 0.55)); */
            /* gradient.addColorStop(1.0, Qt.rgba(0, 0, 0, 0.65)); */
            ctx.fillStyle = fillColor
            ctx.fill()
            ctx.restore()
        }
    }


    DropShadow {
        anchors.fill: canvas
        horizontalOffset: shadowDirection == "left" ? -1 : 1
        verticalOffset: 1
        radius: 3.0
        samples: 16
        color: Qt.rgba(0.0, 0.0, 0.0, 1.0)
        source: canvas
    }    
    
    Item {
        id: container
        x: rect.contentRect.x + borderMargin
        y: rect.contentRect.y + borderMargin
        width: rect.contentRect.width - borderMargin * 2
        height: rect.contentRect.height - borderMargin * 2
    }
}
