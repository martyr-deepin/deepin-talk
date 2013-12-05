import QtQuick 2.0
import QtGraphicalEffects 1.0

Item {
    width: 320;
    height: 240;

	Image {
		anchors.fill: parent
		source: "/home/evilbeast/project/deepin-talk/src/ui/image/bg.png"
	}
	
    Item {
        id: container;
        anchors.centerIn: parent;
        width:  rect.width  + (2 * rectShadow.radius);
        height: rect.height + (2 * rectShadow.radius);

        Rectangle {
            id: rect
            width: 300;
            height: 50;
			color: "#25252522"
            radius: 7;
            antialiasing: true;
            border {
                width: 1;
                color: Qt.rgba(0, 0, 0, 0.2);
            }
            anchors.centerIn: parent;
        }
    }
	
    DropShadow {
        id: rectShadow;
        anchors.fill: container
        cached: true
        /* horizontalOffset: -1 */
        verticalOffset: 2
        radius: 5.0
        samples: 16
        color: "#ffffff"
        smooth: true
        source: container
    }
}