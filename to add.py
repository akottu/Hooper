@app.route('/edit-player/<name>', methods=['GET', 'POST'])
def edit_player(name):
    player = db.session.query(models.Players)\
        .filter(models.Players.name == name).first()
    form = forms.PlayerEditFormFactory.form(player)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            player.player_id = form.player_id.data
            db.session.commit()
            return redirect(url_for('view_players'))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-player.html', player=player, form=form)
    else:
        return render_template('edit-player.html', player=player, form=form)

@app.route('/edit-team/<name>', methods=['GET', 'POST'])
def edit_team(name):
    player = db.session.query(models.Teams)\
        .filter(models.Teams.name == name).first()
    form = forms.TeamEditFormFactory.form(team)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            player.team_id = form.team_id.data
            db.session.commit()
            return redirect(url_for('view_teams'))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-team.html', team=team, form=form)
    else:
        return render_template('edit-team.html', team=team, form=form)


@app.route('/edit-game/<name>', methods=['GET', 'POST'])
def edit_game(gameID):
    player = db.session.query(models.Games)\
        .filter(models.Games.game_id == gameID).first()
    form = forms.GameEditFormFactory.form(game)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            player.game_id = form.game_id.data
            db.session.commit()
            return redirect(url_for('view_games'))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-game.html', game=game, form=form)
    else:
        return render_template('edit-game.html', game=game, form=form)
