function deleteComment() {
    let execute = confirm("Delete comment?")

    if (execute) {
        return true
    } else {
        return false
    }
}

function deleteImage() {
    let execute = confirm("Delete image?")

    if (execute) {
        return true
    } else {
        return false
    }
}

function editImageTitle() {
    let execute = confirm("Change title?")

    if (execute) {
        return true
    } else {
        return false
    }
}

function makeAdmin() {
    let execute = confirm("Change user admin status?")

    if (execute) {
        return true
    } else {
        return false
    }
}

function deleteUser() {
    let execute = confirm("Delete this user?")

    if (execute) {
        return true
    } else {
        return false
    }
}