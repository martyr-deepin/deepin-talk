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

    property int blurRadius: 16
    property int blurWidth: 10
    property int borderWidth: 2
    property int rectRadius: 4
    property rect contentRect

    Canvas {
        id: canvas
        width: rect.width
        height: rect.height
        
        onWidthChanged: requestPaint()        
        onHeightChanged: requestPaint()
        
        onPaint: {
            var ctx = getContext("2d")

            ctx.save()
            ctx.clearRect(0, 0, canvas.width, canvas.height)

            ctx.beginPath();

            var x = blurWidth
            var y = blurWidth
            var w = rect.width - 2 * blurWidth
            var h = rect.height - 2 * blurWidth
            rect.contentRect = Qt.rect(x, y, w, h)
            ctx.roundedRect(x, y, w, h, rectRadius, rectRadius)
            ctx.closePath()

            ctx.lineWidth = borderWidth
            ctx.strokeStyle = borderColor
            ctx.stroke()

            var gradient = ctx.createLinearGradient(rect.width / 2, 0, rect.width / 2, rect.height);
            gradient.addColorStop(0.0, Qt.rgba(0, 0, 0, 0.55));
            gradient.addColorStop(1.0, Qt.rgba(0, 0, 0, 0.65));
            ctx.fillStyle = gradient
            ctx.fill()
            ctx.restore()
        }
    }

    Glow {
        anchors.fill: canvas
        visible: rect.withBlur
        radius: blurRadius
        samples: 16
        color: rect.blurColor
        source: canvas
    }
    
    Item {
        id: container
        x: rect.contentRect.x + borderMargin
        y: rect.contentRect.y + borderMargin
        width: rect.contentRect.width - borderMargin * 2
        height: rect.contentRect.height - borderMargin * 2
        anchors.centerIn: parent

    }
}
