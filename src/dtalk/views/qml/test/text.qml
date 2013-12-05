import QtQuick 2.1
import QtGraphicalEffects 1.0


Item {
	width: 600; height: 300
	
	Image {
		anchors.fill: parent
		source: "/home/evilbeast/project/deepin-talk/src/ui/image/bg.png"
	}
	
	
	Rectangle {
		width: 300; height: 200
		border { width: 2; color: "white"}
        color: "orange"
		radius: 5
		
		
		
		DropShadow {
			anchors.fill: parent
			horizontalOffset: 3
			verticalOffset: 3
			radius: 8.0
			samples: 16
			color: "#80000000"
			source: parent
		}		
	}
	
}