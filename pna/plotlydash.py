import json
from typing import Dict, List, Optional

from dash import callback_context, Dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import pandas as pd
import plotly.express as px

from pna.logic import Logic


def in_a_row(*args, id='', margin: str = '2%', style: Dict = None,
             width: Optional[str] = None) -> html.Div:
    wrappers = []
    for item in args:
        item_style = dict(float='left', clear='none', margin=margin)
        if width is not None:
            item_style['width'] = width
        wrappers.append(html.Div(
            children=[item],
            style=item_style))
    return html.Div(id=id, children=wrappers, style=style)


def in_a_line(*args, margin: str = '2%', id: str = '', style: Dict = None):
    wrappers = []
    for item in args:
        wrappers.append(html.Div(
            children=[item],
            style=dict(float='left', clear='both', margin=margin)))
    return html.Div(id=id, children=wrappers, style=style)


def radio(label: str,
          id: str,
          options: List[str],
          selection: Optional[str] = None,
          style: Optional[Dict] = None):
    label = html.Span(children=[label])
    control = dcc.RadioItems(
        id=id,
        options=[{'label': x, 'value': x} for x in options],
        value=selection)
    return in_a_row(label, control, style={'float': 'left', 'clear': 'both'})


def button(id: str, label: str, style=dict(float='left', clear='none')):
    return html.Button(id=id, n_clicks=0, children=[label], style=style)


def hidden_div(id: str, children: list = [], className: Optional[str] = None):
    return html.Div(id=id, children=children, style=dict(display='none'),
                    className=className)


def data_table(df: pd.DataFrame,
               columns: Optional[List[str]] = None,
               id: str = '',
               edit_rows: bool = False,
               select_rows: Optional[str] = False,
               delete_rows: bool = False,
               page_size=50):
    if columns is None:
        columns = df.columns
    columns = [{'name': x, 'id': x} for x in columns]
    return dash_table.DataTable(
        id=id,
        columns=columns,
        data=df.to_dict('records'),
        sort_action='native',
        sort_mode='native',
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        editable=edit_rows,
        row_selectable=select_rows,
        row_deletable=delete_rows,
        page_size=page_size,
        export_format='csv')


def init_dashboard(server):
    dash_app = Dash(
        server=server,
        routes_pathname_prefix='/propaganda_analysis/',
        external_stylesheets=[
            'static/style.css'
        ]
    )

    # layout
    dash_app.layout = html.Div(children=[
        # options
        html.H2('Corpus',
                style={'float': 'left', 'clear': 'all'}),
        document_set_selector(),
        initialize_button(),

        # corpus information
        html.Div(
            id='entities_and_liwc',
            children=[
                html.Div(
                    id='top_entities_wrapper',
                    style=dict(float='left', width='40%', margin='2%'),
                    children=[top_entities_plot()]),
                html.Div(
                    id='corpus_volume_wrapper',
                    style=dict(float='left', width='40%', height='100%',
                               margin='2%', clear='none'),
                    children=[corpus_attention_plot()]
                ),
            ],
            style=dict(float='left', clear='both', width='100%')),

        html.Div(
            id='liwc_over_time_wrapper',
            style=dict(float='left', clear='both', width='100%'),
            children=dcc.Graph(id='liwc_over_time')),

        html.H2('Entity Analysis',
                style={'float': 'left', 'clear': 'both'}),

        # entity selection
        word_selection_controls(),

        # entity attention and liwc
        html.Div(
            id='entity_attention_plot_wrapper',
            children=[entity_attention_plot()],
            style=dict(float='left', width='40%', height='100%',
                       margin='2%', clear='none')),
        html.Div(
            id='entity_liwc_plot_wrapper',
            children=[entity_liwc_plot()],
            style=dict(float='left', width='40%', height='100%',
                       margin='2%', clear='none')),

        # word vectors
        hidden_word_vec_data_div(),
        word_vec_plot(),

        html.H2(children='Narrative Analysis',
                style={'float': 'left', 'clear': 'both'}),

        # sentence view
        html.H3(children='Tweet Explorer',
                style={'float': 'left', 'clear': 'both'}),

        sentence_selector(),
        in_a_row(
            sentences(),
            html.Div(
                id='sentence_context_wrapper',
                children=[sentence_context()]),
            width='80%',
            style=dict(clear='both')),

        # # set of narratives
        # html.Div(
        #     id='narratives_div',
        #     children=[
        #         in_a_row(
        #             in_a_line(
        #                 html.H3(children='Manage Narratives List',
        #                         style={'float': 'left', 'clear': 'both'}),
        #                 html.Div(
        #                     id='narratives_left_panel',
        #                     children=[html.Div(id='narrative_list')],
        #                     style=dict(float='left', width='40%', margin='2%')),
        #                 html.Div(
        #                     id='narratives_right_panel',
        #                     children=[create_narrative_form()],
        #                     style=dict(float='left', width='40%', margin='2%',
        #                                clear='none'))),
        #             in_a_line(
        #                 html.H3(children='Tag Narratives',
        #                         style={'float': 'left', 'clear': 'both'}),
        #                 html.Div(id='tagged_narrative_explorer_div'),
        #                 tag_narrative())
        #         ),
        #     ],
        #     style=dict(float='left', clear='both', width='100%')),

        # tagging form and tagged data explorer


        hidden_div(id='tagged_data'),
    ])

    # callbacks
    init_callbacks(dash_app, dash_app.server.logic)

    return dash_app.server


#
# form elements


def document_set_selector():
    # so far just giving the options of Taiwan (zh) and Twitter (en)
    return radio(
        label='Document Set:',
        id='document_set',
        options=['Phillipines Embassy (en)'],
        selection='Phillipines Embassy (en)')


def initialize_button():
    return button(id='initialize', label='Initialize',
                     style=dict(display='none'))


def top_entities_plot():
    # prior initialization, just return an empty div
    return html.Div(id='top_entities')


def corpus_attention_plot():
    return dcc.Graph(id='corpus_attention')


def word_selection_controls():
    return html.Div(
        id='word_selection_controls',
        children=[
            in_a_line(
                in_a_row(
                    html.Span('Choose an entity from the above list:'),
                    dcc.Input(id='word_for_vectors', type='text'),
                    html.Button(id='update_word_selection',
                                children=['Update'])),
                html.Div(id='word_selection_error_message'))
        ],
        style=dict(float='left', clear='both', width='100%'))


def entity_attention_plot():
    return html.Div(
        id='entity_attention_wrapper',
        children=[dcc.Graph(id='entity_attention')],
        style=dict(display='none')
    )


def hidden_word_vec_data_div():
    return hidden_div(id='word_vec_data')


def word_vec_plot():
    return html.Div(
        id='word_vec_plot_div',
        children=[dcc.Graph(id='word_vec_plot')],
        style=dict(float='left', clear='both', display='none'))


def entity_liwc_plot():
    return html.Div(
        id='entity_liwc_plot_div',
        children=[dcc.Graph(id='entity_liwc_plot')],
        style=dict(display='none'))


def create_narrative_form():
    return html.Div(
        id='narrative_form',
        children=[
            hidden_div(
                id='narrative_form_state',
                children=[json.dumps(dict(
                    complete=True,
                    last_action='init',
                    messages=[]))]),
            in_a_line(
                # first row
                in_a_row(
                    html.Span('Pick a Short Code (6 letters):'),
                    dcc.Input(id='narrative_code', type='text'),
                    button(id='delete_narrative_button', label='Delete'),
                    hidden_div(
                        id='confirm_delete_narrative_controls',
                        children=[
                            in_a_row(
                                button(id='confirm_delete_narrative',
                                          label='Confirm Delete'),
                                button(id='cancel_delete_narrative',
                                          label='Cancel Delete')
                            )])
                ),
                html.Span('Description:'),
                dcc.Input(
                    id='narrative_description',
                    type='text',
                    style=dict(width='300px')),
                button(id='create_narrative', label='Create Narrative'),
                html.Div(id='narrative_form_messages', style=dict(color='red'))
            ),
        ]
        # NOTE: styled by the outer container
    )


def sentence_selector():
    return in_a_row(
        html.Span('View sentences containing words (separate with ,):'),
        dcc.Input(id='keywords_for_sentences', type='text'),
        button(id='find_sentences', label='Find Sentences'),
        id='sentence_selector_form',
        style=dict(width='100%'))


def sentences():
    # prior to initialization, just return an empty div
    # hide until ready to show
    return html.Div(
        id='sentences_wrapper',
        children=[
            hidden_div(id='sentence_data'),
            html.Div(id='sentences_div',
                     children=data_table(
                        id='sentences_table',
                        df=pd.DataFrame({'Date': [],
                                         'Url': [],
                                         'Likes': [],
                                         'Retweets': []}),
                        columns=['Date', 'Url', 'Likes', 'Retweets'],
                        page_size=10)
                     )])


def sentence_context(context: Optional[Dict] = None):
    if context is None:
        context = {'source': '', 'title': '', 'url': '', 'paragraph': ''}
    return in_a_line(
        html.H4(children=context['title']),
        dcc.Link(
            href=context['url'],
            children=[context['source']],
            target='_blank'),
        html.Div(id='paragraph_text', children=[context['paragraph']]))


def tag_narrative():
    return html.Div(
        id='tag_narrative_form',
        children=[
            in_a_line(
                in_a_row(
                    html.Span('Annotator (your name):'),
                    dcc.Input(id='annotator', type='text')),
                in_a_row(
                    html.Span('Text:'),
                    dcc.Input(id='annotated_text',
                              type='text',
                              style=dict(width='800px'))),
                in_a_row(
                    html.Span('with narrative code:'),
                    # NOTE: load on initial call
                    dcc.Dropdown(
                        id='narrative_tag_code',
                        options=[],
                        value='',
                        style=dict(width='150px'))),
                button(id='tag_narrative', label='Tag Narrative'))])


def download_csv():
    return html.A(
        'Download Data',
        id='download_csv',
        download='placeholder.csv',
        href='',
        target="_blank"
    )


# callbacks


def init_callbacks(dash_app, logic: Logic):
    # 1. Hitting initialize button:
    #   - loads top entities
    # 2. Updating the word selection:
    #   - updates vector plot
    #   - updates liwc rep
    # 3. add/edit on narratives form
    #   - add or edit a narrative
    # 4. delete on narratives form
    #   - delete a narrative
    # 5. Update sentences selection
    #   - reload sentences table
    # 6. add narrative tag
    #   - add tag to db
    # 7. remove narrative tag
    #   - remove tag from db
    #
    # Don't see any dependencies here... just straight of the bat.

    @dash_app.callback(
        Output('top_entities', 'children'),
        [Input('initialize', 'n_clicks')])
    def init_top_entities(n_clicks: int):
        ents = logic.entity_counts()
        return data_table(df=ents, page_size=15)

    @dash_app.callback(
        Output('corpus_attention', 'figure'),
        [Input('initialize', 'n_clicks')])
    def init_corpus_attention(n_clicks: int):
        df = logic.corpus_volume_over_time()
        return px.bar(
            data_frame=df,
            x='Date',
            y='Count',
            title='Tweet Volume over Time')

    @dash_app.callback(
        Output('liwc_over_time', 'figure'),
        [Input('initialize', 'n_clicks')])
    def init_liwc_time(n_clicks: int):
        df = logic.liwc_over_time()
        return px.bar(
            data_frame=df,
            x='Date',
            y='Frequency',
            color='Category',
            title='Types of words over time')

    @dash_app.callback(
        Output('word_selection_error_message', 'children'),
        [Input('update_word_selection', 'n_clicks'),
         State('word_for_vectors', 'value')],
        prevent_initial_call=True)
    def update_word_selection_error_message(n_clicks: int, word: str):
        valid = logic.in_vocab(word)
        if not valid:
            return f'"{word}" not prepared for analysis - please choose ' \
                   f'another word from the entity list.'
        else:
            return ''

    @dash_app.callback(
        Output('word_vec_data', 'children'),
        [Input('word_selection_error_message', 'children'),
         State('word_for_vectors', 'value'),
         State('word_vec_data', 'children')],
        prevent_initial_call=True)
    def get_vec_liwc_and_entity_attention_data(
            message: str,
            word: str,
            previous_data: str):
        if message != '':
            return ''
        neighbours = logic.vector_neighbourhood(word)
        liwc = logic.liwc_profile(word)
        attention = logic.entity_counts_over_time(word)
        data = {
            'neighbours': neighbours.to_json(orient='split'),
            'liwc_freqs': liwc.to_json(orient='split'),
            'entity_attention': attention.to_json(orient='split')
        }
        return json.dumps(data)

    @dash_app.callback(
        Output('entity_attention', 'figure'),
        [Input('word_vec_data', 'children'),
         State('word_for_vectors', 'value')],
        prevent_initial_call=True)
    def update_entity_attention(json_data: str, entity: str):
        json_data = json.loads(json_data)['entity_attention']
        df = pd.read_json(json_data, orient='split')
        return px.bar(
            data_frame=df,
            x='Date',
            y='Count',
            title=f'Attention to {entity}')

    @dash_app.callback(
        Output('entity_attention_wrapper', 'style'),
        [Input('word_vec_data', 'children')],
        prevent_initial_call=True)
    def show_entity_attention(json_data: str):
        return dict(display=True)

    @dash_app.callback(
        Output('word_vec_plot', 'figure'),
        [Input('word_vec_data', 'children'),
         State('word_for_vectors', 'value')],
        prevent_initial_call=True)
    def update_word_vec_plot(json_word_vec_data: str, entity: str):
        json_data = json.loads(json_word_vec_data)['neighbours']
        df = pd.read_json(json_data, orient='split')
        return px.scatter(
            data_frame=df,
            x='PC1',
            y='PC2',
            text='token',
            opacity=0.,
            height=1000,
            width=1600,
            title=f'Words similar to {entity}')

    @dash_app.callback(
        Output('entity_liwc_plot', 'figure'),
        [Input('word_vec_data', 'children'),
         State('word_for_vectors', 'value')],
        prevent_initial_call=True)
    def update_entity_liwc_plot(json_word_vec_data: str, word: str):
        json_data = json.loads(json_word_vec_data)['liwc_freqs']
        df = pd.read_json(json_data, orient='split')
        return px.bar(
            data_frame=df,
            x='NPMI',
            y='Category',
            height=550,
            title=f'Types of words around {word}')

    @dash_app.callback(
        Output('entity_liwc_plot_div', 'style'),
        [Input('word_vec_data', 'children')],
        prevent_initial_call=True)
    def show_entity_liwc_plot(json_data: str):
        display = json_data is not None
        return dict(display=display)

    @dash_app.callback(
        Output('word_vec_plot_div', 'style'),
        [Input('word_vec_data', 'children')],
        prevent_initial_call=True)
    def show_word_vec_plot(json_data: str):
        display = json_data is not None
        return dict(float='left', clear='both', display=display)

    @dash_app.callback(
        Output('sentence_selector_form', 'style'),
        [Input('word_vec_data', 'children')],
        prevent_initial_call=True)
    def show_sentence_selector_form(json_data: str):
        display = json_data is not None
        return dict(float='left', clear='both', display=display)

    @dash_app.callback(
        Output('sentences_wrapper', 'style'),
        [Input('find_sentences', 'n_clicks')],
        prevent_initial_call=True)
    def show_sentences_data(n_clicks: int):
        # basically: hide on load, and show after first search
        return dict(float='left', clear='both', display=True)

    @dash_app.callback(
        Output('sentences_div', 'children'),
        [Input('sentence_data', 'children')],
        prevent_initial_call=True)
    def load_sentences(json_data: str):
        df = pd.read_json(json_data, orient='split')
        return data_table(
            id='sentences_table',
            df=df,
            columns=['Date', 'Url', 'Likes', 'Retweets'],
            page_size=10)

    @dash_app.callback(
        Output('sentence_data', 'children'),
        [Input('find_sentences', 'n_clicks'),
         State('keywords_for_sentences', 'value'),
         State('word_for_vectors', 'value')],
        prevent_initial_call=True)
    def get_sentence_data(n_clicks: int, keywords: str, entity: str):
        df = logic.sentences(entity)
        if keywords:
            if ',' in keywords:
                keywords = [k.lower() for k in keywords.split(',')]
            else:
                keywords = [keywords.lower()]
            df['lower'] = df.Sentence.apply(lambda x: x.lower())
            df['keep'] = df.Sentence.apply(
                lambda x: any(k in x for k in keywords))
            df = df[df.keep == True]
        return df.to_json(orient='split')

    #
    # narrative form

    # update state - also handle creating and deleting as hook up buttons here
    @dash_app.callback(
        Output('narrative_form_state', 'children'),
        [Input('delete_narrative_button', 'n_clicks'),
         Input('confirm_delete_narrative', 'n_clicks'),
         Input('cancel_delete_narrative', 'n_clicks'),
         Input('create_narrative', 'n_clicks'),
         State('narrative_code', 'value'),
         State('narrative_description', 'value')],
        prevent_initial_call=True)
    def update_narrative_form_state(nc1, nc2, nc3, nc4, code, description):
        # determine which button was clicked
        button = callback_context.triggered[0]['prop_id'].split('.')[0]

        if button == 'confirm_delete_narrative':
            logic.dbi.narratives.delete(code)
        if button == 'create_narrative':
            logic.dbi.narratives.create(code, description)
        narratives = logic.dbi.narratives.all()

        state = dict(
            complete=button in ['confirm_delete_narrative', 'create_narrative'],
            last_action=button,
            narratives=narratives.to_json(orient='split'),
            messages=[])

        return json.dumps(state)

    # use state to decide whether to show or hide delete confirmation
    @dash_app.callback(
        Output('confirm_delete_narrative_controls', 'style'),
        [Input('narrative_form_state', 'children')],
        prevent_initial_call=True)
    def show_or_hide_narrative_delete_confirmation_controls(state):
        state = json.loads(state)
        if state['last_action'] == 'delete_narrative_button':
            display = True
        else:
            display = 'none'
        style = dict(float='left', clear='none', display=display)
        return style

    # use state to decide whether to disable code for delete confirmation
    @dash_app.callback(
        Output('narrative_code', 'disabled'),
        [Input('narrative_form_state', 'children')],
        prevent_initial_call=True)
    def enable_or_disable_narrative_code(state):
        state = json.loads(state)
        return state['last_action'] == 'delete_narrative_button'

    # update narrative list
    @dash_app.callback(
        Output('narrative_list', 'children'),
        [Input('narrative_form_state', 'children')],
        prevent_initial_call=False)  # do populate on load
    def reload_narrative_list(json_data: str):
        # determine which button was clicked
        if isinstance(json_data, list):
            df = logic.dbi.narratives.all()
        else:
            json_data = json.loads(json_data)
            df = pd.read_json(json_data['narratives'], orient='split')
        df.rename(
            columns={'code': 'Code', 'description': 'Description'},
            inplace=True)
        return data_table(df=df, page_size=10)

    # set code and narrative to nothing after completing action
    @dash_app.callback(
        [Output('narrative_code', 'value'),
         Output('narrative_description', 'value')],
        [Input('narrative_form_state', 'children'),
         State('narrative_code', 'value'),
         State('narrative_description', 'value')],
        prevent_initial_call=True)
    def reset_narrative_form(state: str, code: str, description: str):
        state = json.loads(state)
        if state['last_action'] \
                in ['confirm_delete_narrative', 'create_narrative']:
            code = ''
            description = ''
        return code, description

    # fill narrative code dropdown options
    @dash_app.callback(
        Output('narrative_tag_code', 'options'),
        [Input('narrative_form_state', 'children')],
        prevent_initial_call=False)
    def load_narrative_code_drop_down(json_data: str):
        if isinstance(json_data, list):
            df = logic.dbi.narratives.all()
        else:
            json_data = json.loads(json_data)
            df = pd.read_json(json_data['narratives'], orient='split')
        options = [{'label': x, 'value': x} for x in df.code]
        df.rename(
            columns={'code': 'Code', 'description': 'Description'},
            inplace=True)
        return options

    # create narrative when submitting form
    @dash_app.callback(
        Output('tagged_data', 'children'),
        [Input('tag_narrative', 'n_clicks'),
         State('annotator', 'value'),
         State('narrative_tag_code', 'value'),
         State('annotated_text', 'value')],
        prevent_initial_call=True)
    def create_narrative_tag(n_clicks: int,
                             annotator: str,
                             code: str,
                             text: str):
        logic.dbi.narrative_labels.create(
            narrative_code=code,
            annotator=annotator,
            text=text)
        data = logic.dbi.narrative_labels.all()
        data = data.to_json(orient='split')
        return data

    # tagged narrative table
    @dash_app.callback(
        Output('tagged_narrative_explorer_div', 'children'),
        [Input('tagged_data', 'children')],
        prevent_initial_call=False)
    def update_tagged_narrative_table(json_data: str):
        if json_data is None or isinstance(json_data, list):
            df = logic.dbi.narrative_labels.all()
        else:
            df = pd.read_json(json_data, orient='split')
        df.rename(
            columns={
                'narrative_code': 'Code',
                'annotator': 'Annotator',
                'text': 'Text',
                'description': 'Description'},
            inplace=True)
        return data_table(df=df, page_size=10)
