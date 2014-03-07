import QtQuick 2.1
import "../scripts/common.js" as Common

DShadow {
	id: rootWindow
    signal closed
    default property alias content: container.children
    property alias titlebarLeftItem: titlebar.leftItem
    property alias titlebarButtons: titlebar.buttons
    property alias titlebarMenu: titlebar.menu
    property alias titlebarMin: titlebar.min
    property alias titlebarMax: titlebar.max
    property alias titlebarClose: titlebar.close
    property int titlebarHeight: Common.titlebarHeight
    
	Item {
		anchors.margins: rootWindow.sideWidth + 1
		anchors.fill: parent
		
		Titlebar {
			id: titlebar
			width: parent.width; height: titlebarHeight
			anchors.top: parent.top
            
			DragArea {
				anchors.fill: parent
				window: windowView
                propagateComposedEvents: true

                onClicked: {
                    mouse.accepted = false
                }
			}
            
            onClosed: {
                rootWindow.closed()
                windowView.closeWindow()
            }
		}
		
		Item {
            id: container
			anchors.top: titlebar.bottom
			width: parent.width
			height: parent.height - titlebar.height
		}

	}
}