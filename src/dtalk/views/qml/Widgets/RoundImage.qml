import QtQuick 2.1
import QtGraphicalEffects 1.0

Item {
	id: container
	
	property alias source: image.source
	property real radius: width/2
	
	Image {
		anchors.fill: parent		
		id: image
		smooth: true
	}
	
	RoundItem {
		target: image
		radius: container.radius
	}
}
	
