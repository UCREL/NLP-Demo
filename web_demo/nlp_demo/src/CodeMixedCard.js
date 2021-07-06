import './index.scss';

import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';

import { CardLabel, InfoTitle } from './CardUtilities';


const moreInfoPopover = (
    [<div key="1">
        Example taken from:<br/>
        <a href="https://www.aclweb.org/anthology/D18-1030.pdf">A Fast, Compact, 
        Accurate Model for Language Identification 
        of Codemixed Text</a> paper. Click the information icon for a link to 
        the paper.
    </div>]
);

const CodeMixedCard = (props) => {
    return (
        <Col xs={12} lg={{span: 10, offset: 1}}>
            <Card.Body>
                <InfoTitle title="Codemixed" info={moreInfoPopover} 
                           showTitleInfo={props.showTitleInfo}
                           setShowTitleInfo={props.setShowTitleInfo}
                />
                <hr/>
            </Card.Body>
            <CardLabel label="Spanish / English" 
                       text={[<span key="1" className="bold underline">dame ese</span>,
                              <span key="2"> book that you told me about</span>]}
                       translation="Give me this book that you told me about"
                       showTranslationText={props.showTranslationText}
                       setShowTranslationText={props.setShowTranslationText} />
            <Card.Body>
                <p>
                    In general texts that contain more than one language (codemixed) is 
                    more difficult to language identify than texts with a single language.
                    This type of language is more common in user-generated texts like Tweets, 
                    3.5% of Tweets are codemixed, as this data is typically user generated
                    this in itself normally brings it's own problems like abbrevations and 
                    mis-spellings. 
                </p>
                <br/>
                <p>
                    Methods for this task are expected to output the 
                    language(s) that are within a text, some methods can even output 
                    the language per word, like the method described in this paper 
                    by Google: <a href="https://www.aclweb.org/anthology/D18-1030.pdf">A 
                    Fast, Compact, Accurate Model for Language Identification of 
                    Codemixed Text</a>.
                </p>
            </Card.Body>
        </Col>
    )
}

export default CodeMixedCard;