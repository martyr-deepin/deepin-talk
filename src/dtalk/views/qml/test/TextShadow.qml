import QtQuick 2.1

Text {
    property Text target;
 
    text: target.text;
    color: "white";
    /* x: target.x + 1; */
    y: target.y + 1;
    font: target.font;
    opacity: target.opacity;
}