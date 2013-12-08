import QtQuick 2.1
import "../scripts/common.js" as Common

DShadow {
	id: root
    default property alias content: container.children
    
	Item {
		anchors.margins: root.sideWidth + 1
		anchors.fill: parent
		
		Titlebar {
			id: titlebar
			width: parent.width; height: Common.titlebarHeight
			anchors.top: parent.top
			DragArea {
				anchors.fill: parent
				window: windowView
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