import QtQuick 2.1
import QtGraphicalEffects 1.0


Text {
	id: target
	property alias shadowColor: shadow.color
	
	Text {
		id: shadow
		text: target.text;
		color: Qt.rgba(0.9, 0.9, 0.9, 0.3)		
		x: 0;
		y: 1;
		font: target.font;
		opacity: target.opacity;
		
	}	

}
