import QtQuick 2.0
import QtGraphicalEffects 1.0

Item {
    width: 300
    height: 300
	
	

    Image {
        anchors.fill: parent
		source: "../../image/bg.png"
    }

	
    /* Image { */
    /*     id: butterfly */
    /*     source: "../../image/butterfly.png" */
    /*     sourceSize: Qt.size(parent.width, parent.height) */
    /*     smooth: true */
    /*     visible: false */
    /* } */
	
	Text {
		id: butterfly
		text: "LinuxDeepin@Gmail.com"
		color: Qt.rgba(0.1, 0.1, 0.2, 1.0)
	}

    InnerShadow {
        anchors.fill: butterfly
        radius: 2.0
        samples: 3
        horizontalOffset:-2
        verticalOffset: -2
        color: "#fff"
        source: butterfly
    }
}