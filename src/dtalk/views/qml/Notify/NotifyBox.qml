import QtQuick 2.1
import "../Widgets"
import QtQuick.Window 2.1

Window {
    id: win
    width: container.width; height: container.height
    x: trayIcon.getPos().x - width / 2
    y: trayIcon.getPos().y - height
    /* visible: trayIcon.hovered || mouseArea.containsMouse */
    flags: Qt.FramelessWindowHint | Qt.Popup
	color: "transparent"
    
    Connections {
        target: trayIcon
        onHoverStatusChanged: {
            if (notifyView.model.total() == 0) {
                if (win.visible) {
                    win.visible = false
                }
                return
            }
            var hovered = trayIcon.hovered
            if (hovered || mouseArea.containsMouse) {
                if (!win.visible) {
                    win.visible = true
                }
            } else {
                if (win.visible) {
                    win.visible = false
                }
            }
        }
    }
    
    RectWithCorner {
        id: container
        cornerHeight: 10
        cornerWidth: 12
        rectWidth: 200
        rectHeight: notifyView.contentHeight + container.blurWidth * 2 + container.cornerHeight + container.borderMargin * 2 + 16
        
        ScrollWidget {
            anchors.fill: parent
            ListView {
                id: notifyView
                anchors.fill: parent
                clip: true
                delegate: NotifyDelegate {}
                model: controlManager.getNotifyModel()
            }
        }
    }
    
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
    }
}
