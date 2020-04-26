function editPlayer(player) {
    alert("Editing player with id " + player.player_id)
}

if($(".home-points").text() > $(".away-points").text()) {
    $(".home-team").css("background-color", "lightblue")
    $(".home-stats").css("background-color", "lightblue")
} else {
    $(".away-team").css("background-color", "lightblue")
    $(".away-stats").css("background-color", "lightblue")
}