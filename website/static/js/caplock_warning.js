function IsCapsLockOn(event) {
    if (event.getModifierState("CapsLock")) {  // If "caps lock" is pressed, display the warning text
        document.getElementById("spnWarning").style.display = "block";
        document.getElementById("spnWarning2").style.display = "block";
    }
    else {
        document.getElementById("spnWarning").style.display = "none";
        document.getElementById("spnWarning2").style.display = "none";
    }
}