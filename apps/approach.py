import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

# --- Approach Page Layout ---

layout = html.Div(
    [
        html.H1(children = 'Approach'),
        html.Br(),

        html.P(children = 'As a disclaimer, chord progressions, in the context of this program, only refer to progressions where no chord appears more than once. This is a significant restriction but it allows for multiplication as discussed below.'),
        html.H4(children = 'What is a Chord Progression?'),
        dcc.Markdown(children = 'From the altered definition above, a chord progression when written is a permutation on a set of chords where the chords are unique symbols in the progression. For example, the progression *C Am Dm G* is a permutation of four symbols.'),
        html.P(children = 'But at its core, a chord progression is a sequence of chords in music, where one chord must move to the next one specified from the progression. This can also be treated as a function that takes a given chord as an input and outputs the chord that follows it in the progression.'),
        html.H4(children = 'Functions'),
        dcc.Markdown(children = 'Any chord inputted into this function has only one unique output: the chord to its immediate right. Like, *f(Am) = Dm* from the example earlier. Since chord progressions represent functions that have exactly one output for all inputs, they also represent bijections (linear functions that are both onto and one-to-one).'),
        html.H4(children = 'The Symmetric Group and Cycles'),
        html.P(children = [
            'The characteristics of a chord progression and its function-like behavior relate to a concept in abstract algebra, specifically group theory. All of the possible permutations on a set of symbols (chord progressions, from our earlier definition) are elements of a ',
            html.Strong(children = 'symmetric group'),
            ' labeled by ',
            html.I(children=['S',html.Sub(children = 'n')]),
            ' where ',
            html.I(children = 'n'),
            ' is the number of unique symbols (chords) in the set. Since chord progressions behave as elements of a symmetric group, chord progressions can take advantage of the symmetric group\'s properties.'
        ]),
        html.P(children = [
            'Certain elements of the symmetric group are also called cycles, which exhibit the same sequential nature of chord progressions. They are written in cycle notation like the following example ',
            html.I(children = '(1 2 3 4)'),
            ', which is an element of the symmetric group ',
            html.I(children=['S',html.Sub(children = '4 ')]),
            '.'
        ]),
        dcc.Markdown(children = 'The numbers, which signify unique symbols, are actually arbitrary, so replacing them with chords yields a new way to write progressions, like the example from earlier: *(C Am Dm G)*.'),
        html.H4(children = 'Multiplying Cycles'),
        html.P(children = 'Cycles belong to a symmetric group and its group operation is function composition, also referred to as multiplication. However, the set of cycles are not closed under symmetric group multiplication. Meaning, the product of two cycles may not be a cycle. The product would instead be a product of cycles but still an element of the symmetric group.'),
        html.P(children = [
            'For example, ',
            html.I(children = '(1 2 3 4)(2 4) = (1 2)(3 4)'),
            '. The end product, ',
            html.I('(1 2)(3 4)'),
            ', is not a cycle but still is an element of ',
            html.I(children=['S',html.Sub(children = '4')]),
            ' since it still represents a permutation of four symbols. The output is shown in its cycle representation as a product of two cycles of length 2. Since this operation is not commutative, both orders of multiplication are included in the output of the website\'s calculator.'
        ]),
        html.P(children = 'And as a reminder, a chord can only appear once in one progression for this algorithm to work. In addition, the two progressions should have at least one chord in common to avoid receiving an output that describes the same progressions as the inputs.'),
        html.H4(children = 'Meaning'),
        html.P(children = 'As an exploratory tool that showcases connections between math and music, the website\'s output can have multiple uses and interpretations through the lens of chord progressions. For instance, the resulting cycles could aid songwriters in composing new progressions. However in general, symmetric group multiplication of chord progressions produces new progressions based on the relationships between chords from both input progressions.'),
        html.Br(),
    ],
    style = {'padding-left' : '10%',
            'padding-right' : '10%',
            'padding-top' : '5%'},
)
