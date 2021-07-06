import './_flex-styles.scss';
import './_ucrel.scss';

import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';



const UCRELToken = (props) => {
    let text = props.token.text;
    let tooltipData = [];
    let _id = "";
    // The USAS label is converted from an N length sequence e.g. T1.2 to a 
    // string that is of length 2 e.g. T1.2 will become T1. This was done so 
    // that we can match on a higher level category for the CSS styling. 
    if ("usas_label" in props.token){
        tooltipData.push(<p key={"usas"}>Semantic label = {props.token.usas_label}</p>);
        _id = props.token.usas_tag.slice(0,2)
    }
    if ("pos_label" in props.token){
        tooltipData.push(<p key={"pos"}>Part Of Speech = {props.token.pos_label}</p>);
    }
    return (
        <OverlayTrigger placement="top" overlay={<Tooltip>{tooltipData}</Tooltip>}>
            <mark className="ucrel-token shadow-sm" id={_id} >
                {text}
            </mark>
        </OverlayTrigger>
    )
    
}

const UCRELSentence = (props) => {
    return (
        <div  className="py-3 flex-wrap flex-start">
            {props.tokens}
        </div>
    )
}


const UCRELDoc = (props) => {
    
    const sentenceIndexes = props.sentenceIndexes;
    const tokens = props.tokens

    // Creates a UCRELSentence object per sentence of tokens
    const sentences = [];
    for (let index of sentenceIndexes) {
        const [startIndex, endIndex] = index;
        const sentenceTokens = [];
        for (let tokenIndex = startIndex; tokenIndex < endIndex; tokenIndex++) {
            sentenceTokens.push(<UCRELToken key={tokenIndex} token={tokens[tokenIndex]}></UCRELToken>);
        }
        sentences.push(<UCRELSentence tokens={sentenceTokens} key={index}/>);
    }
    
    return (
        <div className="ucrel-doc">
                {sentences}
        </div>
    )
}

export default UCRELDoc