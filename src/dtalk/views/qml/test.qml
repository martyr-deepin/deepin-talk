import QtQuick 2.0
import QtGraphicalEffects 1.0
import QtQuick.Layouts 1.0

Item {
    width: 800;
    height: 600;

	Image {
		anchors.fill: parent
		source: "image/bg.png"
	}
	
	ColumnLayout {
		anchors.fill: parent

		
		ShadowPanel {

			Layout.fillWidth: true
			height: 50
			TextShadow {
				anchors.centerIn: parent
				text: "linuxdeepin"
			}
		}
		
		ShadowPanel {
			/* Layout.column: 1			 */
			Layout.fillWidth: true
			height: 50
			TextShadow {
				anchors.centerIn: parent
				text: "linuxdeepin"
			}
		}
		
		MaskRoundImage {
			/* source: "http://e.hiphotos.baidu.com/image/w%3D2048/sign=ea5c9dd4d009b3deebbfe368f8876d81/c9fcc3cec3fdfc032e57d904d53f8794a4c2265a.jpg" */
			source: "http://tp3.sinaimg.cn/1908513890/180/40021733468/1"
			width: 80; height: 80
		}
		
	}
	
}