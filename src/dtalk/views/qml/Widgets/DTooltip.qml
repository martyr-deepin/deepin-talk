import QtQuick 2.1
import QtGraphicalEffects 1.0
import DTalk 1.0

DialogCorner {
    id: container
    fillColor: Qt.rgba(1, 1, 1, 0.9)
    borderColor: Qt.rgba(0, 0, 0, 0.15)
    rectWidth: label.width + widthMargin
    rectHeight: 18 + heightMargin
    cornerWidth: 9
    cornerHeight: 6
    cornerDirection: "up"
    cornerPos: 40
    rectRadius: 2
    property alias text: label.text
    
    PopupItem {
        anchors.fill: parent
        windowObject: windowView
        parentObject: container
    }
    
    function show(text) {
        label.text = text
        container.visible = true
        timer.restart()
    }
        
    Item {
        LayoutText {
            id: label
            y: 1            
            minWidth: 100
            font.pixelSize: 12
        }
        
        Timer {
            id: timer
            interval: 2000
            onTriggered: {
                container.visible = false
            }
        }

    }
    
}
