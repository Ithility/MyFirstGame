import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from random import randint

app = dash.Dash(__name__)

h1_style = {
    'color': '#ae00ff',
    'size': '10px 20px'
}

body_style = {
    'margin-top': '0px',
    'margin-right': '0px',
    'margin-bottom': '0px',
    'margin-left': '0px'
}

button_style = {
    'margin': '5px',
    'padding': '10px 20px',
    'background-color': '#00e1ff',
    'color': 'white',
    'border': 'none',
    'border-radius': '0px',
    'cursor': 'pointer'
}

container_style = {
    'position': 'absolute',
    'top': '0',
    'left': '0',
    'width': '100%',
    'height': '100%',
    'display': 'flex',
    'flex-direction': 'column',
    'align-items': 'center',
    'justify-content': 'center',
    'background-color': '#6f00ff',
    'border': '10px solid #6f00ff',
    'border-bottom': '0px',
    'border-radius': '0px',
}

app.layout = html.Div(style={**body_style, **container_style}, children=[
    html.H1("Number Guessing Game"),
    html.H2("Guess the number from 1 to 3500"),
    html.Label("Enter your guess:"),
    dcc.Input(id='guess', type='number', value=''),
    html.Button('Check', id='submit-val', n_clicks=0, style=button_style),
    html.Button('New Game', id='new-game', n_clicks=0, style=button_style),
    html.P(id='result'),
])

def generate_new_number():
    return randint(0, 3500)

x = generate_new_number()  # Generate the initial random number

# Callback to trigger 'Check' button on 'Enter' key press within input field
@app.callback(
    Output('submit-val', 'n_clicks'),
    Input('guess', 'n_submit'),
    State('guess', 'value')
)
def trigger_check_button(n_submit, user_input):
    if n_submit is not None:
        return n_submit + 1
    return 0

# Callbacks to handle other functionalities (e.g., checking the guess, starting a new game)
@app.callback(
    Output('result', 'children'),
    Input('submit-val', 'n_clicks'),
    Input('new-game', 'n_clicks'),
    Input('guess', 'value')
)
def check_guess(submit_clicks, new_game_clicks, user_input):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'new-game' in changed_id:
        global x
        x = generate_new_number()  # Generate a new number for a new game
        return ""
    elif 'submit-val' in changed_id:
        if submit_clicks > 0:
            if user_input is None or user_input == '':
                return "Please type a number."
            try:
                user_input = int(user_input)
                if user_input > x:
                    return html.Img(src='/assets/down.jpg.', style={'width': '50px', 'height': 'auto'})
                elif user_input < x:
                    return html.Img(src='/assets/up.jpg', style={'width': '50px', 'height': 'auto'}),

                else:
                    return html.Img(src='/assets/win.jpg', style={'width': '100px', 'height': 'auto'})
            except ValueError:
                return "Please type a valid number."

if __name__ == '__main__':
    app.run_server(debug=True)

