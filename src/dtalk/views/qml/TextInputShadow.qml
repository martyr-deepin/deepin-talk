import QtQuick 2.1
import QtGraphicalEffects 1.0


TextInput {
	id: target
	property alias shadowColor: shadow.color
	
	/* cursorDelegate: Component { */
	/* 	Rectangle { */
	/* 		id: _cursor */
	/* 		color: shadow.color */
	/* 		width: 2 */
			
	/* 		SequentialAnimation { */
	/* 			id: animation */
	/* 			PropertyAction { target: _cursor; property: "visible"; value: false } */
	/* 			PauseAnimation { duration: 200 } */
	/* 			PropertyAction { target: _cursor; property: "visible"; value: true } */
	/* 			loops: Animation.Infinite */
	/* 			running: true */
	/* 		}			 */
	/* 	} */
	/* } */
	
	Text {
		id: shadow
		text: target.displayText;
		color: Qt.rgba(0.9, 0.9, 0.9, 0.3)		
		x: contentWidth - parent.width > 0 ? 0 - (contentWidth - parent.width) : 0
		y: 1;
		font: target.font;
		opacity: target.opacity;
		
	}	

}
