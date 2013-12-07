import QtQuick 2.0
import QtGraphicalEffects 1.0
import QtQuick.Layouts 1.0

Item {
    width: 300;
    height: 600;

	Image {
		anchors.fill: parent
		source: "image/bg.png"
	}
    
    ListView {
        anchors.fill: parent
        model: 5
        delegate: GroupDelegate {}
    }
}

