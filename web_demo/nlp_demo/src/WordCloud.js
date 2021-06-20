import React, { useState, useEffect } from 'react';
import { TagCloud } from 'react-tagcloud'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';

import { InfoTitle, getJSONData, LoadObject } from './Utilities';


const defaultRenderer = (tag, size, color) => {
    const styles = {
        margin: '3px',
        padding: '3px',
        verticalAlign: 'middle',
        display: 'inline-block',
        color: `black`,
    };
    const { className, style, ...props } = tag.props || {};
    const fontSize = tag.fontSize + 'px';
    const key = tag.key || tag.value;
    const tagStyle = { ...styles, fontSize, ...style };
  
    let tagClassName = 'tag-cloud-tag';
    if (className) {
      tagClassName += ' ' + className;
    }
    
    return (
      <span className={tagClassName} style={tagStyle} key={key} {...props}>
        {tag.value}
      </span>
    )
  }
  
function Options(props) {
    
    const minFontSize = props.minimumFontSize;
    const maxFontSize = props.maximumFontSize;
    // Ensures that minimum and maximum have a font size difference of 6
    const maxFontSizeOptions = [];
    for (let i = (minFontSize + 6); i <= 100; i++){
        maxFontSizeOptions.push(<option value={i} key={i}>{i}</option>);
    }
    const minFontSizeOptions = [];
    for (let i = 0; i <= (maxFontSize - 6); i++){
        minFontSizeOptions.push(<option value={i} key={i}>{i}</option>);
    }


    const fontSizeInfo = `Choose the minimum and maximum font sizes, the most 
                          significant word would have the maximum font size, 
                          whereas the least significant would have the minimum 
                          font size.`;

    return (
        <div>
            <Row className="pt-3 no-select">
                <Col xs={12} lg={6} className="flex flex-center mb-3">
                    <label className="pr-3 no-margin" htmlFor="number-of-words">
                        Number of words: {props.numberWords}
                    </label>
                    <input type="range" id="number-of-words" 
                        name="number-of-words" min="10" max="200" step="10" 
                        defaultValue={props.numberWords} 
                        onChange={(event) => {props.setNumberWords(event.target.value)}}
                        />
                </Col>
                <Col xs={12} lg={6} className="flex flex-center mb-3">
                    <label className="pr-3 no-margin"
                            htmlFor="significance-measure">Choose a significance measure:</label>

                    <select
                            name="significance-measure" 
                            id="significance-measure"
                            value={props.significanceMeasure} 
                            onChange={(event) => {props.setSignificanceMeasure(event.target.value)}}>
                        <option value="Log Likelihood">Log Likelihood</option>
                        <option value="Log Ratio">Log Ratio</option>
                        <option value="Frequency">Frequency</option>
                    </select> 
                </Col>
            </Row>
            <hr style={{width: "80%"}}/>
            <Row className="pt-3 no-select">
                <InfoTitle title="Font Size" info={fontSizeInfo} 
                           infoPlacementDirection="bottom"/>
                <Col xs={12} lg={6} className="flex flex-center pt-3 pb-3" >
                    <label className="pr-3 no-margin"
                            htmlFor="minimum-font-size">Minimum Font Size:</label>
                    <select
                            name="minimum-font-size" 
                            id="minimum-font-size"
                            value={minFontSize}
                            onChange={(event) => 
                                        {
                                            const value = Number.parseInt(event.target.value);
                                            props.setMinimumFontSize(value);
                                        }}>
                        {minFontSizeOptions}
                    </select>
                </Col>
                <Col xs={12} lg={6} className="flex flex-center pt-3 pb-3" >
                    <label className="pr-3 no-margin"
                                htmlFor="maximum-font-size">Maximum Font Size:</label>
                    <select
                            name="maximum-font-size" 
                            id="maximum-font-size"
                            value={maxFontSize}
                            onChange={(event) => 
                                        {
                                            const value = Number.parseInt(event.target.value);
                                            props.setMaximumFontSize(value);
                                        }}>
                        {maxFontSizeOptions}
                    </select>
                </Col>
            </Row>
        </div>
    )
}

function WordCloud() {

    const [wordCloudData, setWordCloudData] = useState({});
    const [numberWords, setNumberWords] = useState(50);
    const [significanceMeasure, setSignificanceMeasure] = useState('Log Likelihood');
    const [minimumFontSize, setMinimumFontSize] = useState(10);
    const [maximumFontSize, setMaximumFontSize] = useState(60);
    
    
    const [toggleOptions, setToggleOptions] = useState(false);
    const [toggleIcon, setToggleIcon] = useState('plus');
    const [toggleSemTags, setToggleSemTags] = useState(false);
    const [dataSource, setDataSource] = useState("/data/thesis_token_statistics.json");


    function binData(minValue, maxValue, numberBins){
        const minMaxDiff = maxValue - minValue;
        const binIntervalStep = Math.round(minMaxDiff / numberBins);
        let binValue = minValue;
        const binIntervalValue = {};
        for (let i=0; i < numberBins - 1; i++){
            binValue += binIntervalStep;
            binIntervalValue[i] = binValue; 
        }
        binIntervalValue[numberBins - 1] = maxValue;
        return binIntervalValue;
    }

    
    
    useEffect( () => {

        function toWordCloudFormat(tagData) {
            let reformatedTagData = [];
            
            for (let token in tagData){
                const data = tagData[token];
                const significanceValue = data[significanceMeasure];
                reformatedTagData.push({ value: token, count: significanceValue});
            }
            reformatedTagData.sort((first, second) => {return second["count"] - first["count"]});
            
            reformatedTagData = reformatedTagData.slice(0, numberWords);
            
            // Setting the font size through the bin interval
            const numberBins = 6;
            const maxValue = reformatedTagData[0]["count"];
            const minValue = reformatedTagData[reformatedTagData.length - 1]["count"];
            const binnedCounts = binData(minValue, maxValue, numberBins);
            const binnedFonts = binData(minimumFontSize, maximumFontSize, numberBins);
    
            for (let index in reformatedTagData){
                const data = reformatedTagData[index];
                const count = data["count"];
                // Need to bin the scaled values in bins of 6
                for (let binInterval in binnedCounts){
                    const countBin = binnedCounts[binInterval];
                    if (count > countBin){
                        continue;
                    }
                    else{
                        data.bin = binInterval;
                        const fontSize = binnedFonts[binInterval]; 
                        data.fontSize = binnedFonts[binInterval];
                        // If you do not add a key it will not re-render when 
                        // you change the font size.
                        data.key = data.value + fontSize.toString();
                        break; 
                    }
                }
            }
    
            // This is sorts the data in alphabetic order.
            function compareStrings(word1, word2){
                word1 = word1.toLowerCase();
                word2 = word2.toLowerCase();
                return word1 > word2  ? 1: -1;
            }
            reformatedTagData.sort((a, b) => {return compareStrings(a["value"], b["value"]); } );
            
            return reformatedTagData;
        }

        let didCancel = false;
        
        getJSONData(process.env.PUBLIC_URL + dataSource)
        .then((value) => {return toWordCloudFormat(value)})
        .then((value) => {
            if (!didCancel){
                setWordCloudData(value)
            }
        })
        .catch(() => {setWordCloudData({'error': true})});

        return () => {didCancel = true};
        
    }, [dataSource, numberWords, minimumFontSize, maximumFontSize, 
        significanceMeasure])

    function changeIconSign(){
        setToggleOptions(!toggleOptions);
        if(toggleOptions){
            setToggleIcon('plus');
        }
        else{
            setToggleIcon('dash');
        }
    }

    function changeDataSource(){
        if (toggleSemTags){
            setDataSource("/data/thesis_token_statistics.json");
        }
        else{
            setDataSource("/data/thesis_tags.json");
        }
        setToggleSemTags(!toggleSemTags);
    }

    let optionsDiv;
    if (toggleOptions) {
        optionsDiv = <div><Options numberWords={numberWords} 
                                  setNumberWords={setNumberWords}
                                  significanceMeasure={significanceMeasure}
                                  setSignificanceMeasure={setSignificanceMeasure}
                                  minimumFontSize={minimumFontSize}
                                  setMinimumFontSize={setMinimumFontSize}
                                  maximumFontSize={maximumFontSize}
                                  setMaximumFontSize={setMaximumFontSize}
                                  />
                    <hr/>
                    </div>;
    }
    else{
        optionsDiv = <hr/>
    }

    function tagCloud(){
        return(<TagCloud className="center-text" minSize={minimumFontSize} 
                         maxSize={maximumFontSize} tags={wordCloudData} 
                         shuffle={false} 
                         renderer={defaultRenderer} />)
    }

    
    return(
        <div className="full-height" id="full-width">
            <div style={{height: "20vh", overflow: "auto", width: "100%"}}>
                <Col xs={12} md={{span: 8, offset: 2}} >
                    <h1>Word Cloud of 3rd year theses</h1>
                    <p className="lead text-muted">
                        Below is a tag cloud showing the top {numberWords} words that 
                        occur significantly more frequently in 3rd year theses than they 
                        would in common English texts. The larger the word the more 
                        significant that words is. The significance measure used below 
                        is {significanceMeasure}.
                    </p>
                    
                    <hr/>
                </Col>
                
            </div>
            
            <div style={{height: "80vh", overflow: "auto", width: "100%"}}>
                
                <Col xs={12} md={{span: 8, offset: 2}}>
                    <div className="pb-3">
                        <span>
                            <span className="bold pr-2 no-select">Options</span>
                            <i onClick={changeIconSign} 
                            className={`bi bi-${toggleIcon}-circle cursor-pointer`}></i>
                        </span>
                    </div>
                    
                
                    {optionsDiv}
                    <div style={{width: "100%"}} className="flex flex-center">
                        <Form.Switch className="no-select" id="sem-tag-switch" 
                                    label="Click to switch between words and Semantic Tags" 
                                    onChange={changeDataSource}
                                    />
                    </div>
                    <hr/>
                </Col>
            
                <LoadObject data={wordCloudData} onSuccess={tagCloud} />
            </div>
        </div>
    )
} 

export default WordCloud; 