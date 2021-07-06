import './index.scss';

import Tooltip from 'react-bootstrap/Tooltip';
import Card from 'react-bootstrap/Card';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tab from 'react-bootstrap/Tab';
import Nav from 'react-bootstrap/Nav';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { InfoTitle } from './CardUtilities';


const moreInfoPopover = (
    [<div key="1">The examples shown here have come from the  
    paper <a rel="noreferrer" target="_blank" href="https://www.aclweb.org/anthology/C18-1113.pdf">Fine-Grained 
    Arabic Dialect Identification</a>, in this paper they release a 
    new dialect identification datasets covering 25 different arabic 
    dialects each from a different city in the Arab World.</div>]
);

const DialectNavLink = (props) => {
    const dialect = props.dialect;
    if ('abbr' in dialect) {
        return (
            <OverlayTrigger key={dialect.key} placement="top" 
                            overlay={<Tooltip> {dialect.abbr} </Tooltip>} >
                <Nav.Link eventKey={dialect.key}>
                    {dialect.language}
                </Nav.Link>
            </OverlayTrigger>
        )
    }
    else{
        return (
            <Nav.Link eventKey={dialect.key}>
                {dialect.language}
            </Nav.Link>
        )
    }
}

const DialectTabNav = (props) => {
    let navArray = [];
    const data = props.data;
    for (const dataIndex in data) {
        const dialect = data[dataIndex];
        navArray.push(
            <Nav.Item className="col text-center" key={dialect.key}>
                <DialectNavLink dialect={dialect} />
            </Nav.Item>
        )
    }
    return (
        <Nav variant="pills" className="flex-col pt-3">
            <Row>
                {navArray}
            </Row>
        </Nav>
    );
}

const DialectTabContent = (props) => {
    let tabs = [];
    const data = props.data;
    for (const dataIndex in data) {
        const dialect = data[dataIndex];
        tabs.push(
        <Tab.Pane eventKey={dialect.key} key={dialect.key}>
            <hr />
            <p className="text-center" lang="ar" dir="rtl">
                {dialect.text}    
            </p>
        </Tab.Pane>);
    }
    return (
        <Tab.Content>
            {tabs}
        </Tab.Content>
    );

}

const DialectCard = (props) => {
    const dialectExamples = [{text: "سوف اخذ هذه , من فضلك ْ", language: "MSA", key: "msa", abbr: "Modern Standard Arabic"},
                             {text: "حناخد هدا , من فضلك ْ", language: "Tripoli", key: "tripoli"},
                             {text: "حاخد ده, اذا سمحتْ", language: "Cairo", key: "cairo"},
                             {text: "رح اخد هاد , ¯ اذا سمحت ْ", language: "Damascus", key: "damascus"}];
    return (
        <Col xs={12} lg={{span: 10, offset: 1}}>
            <Card.Body>
                <InfoTitle title="Dialects" info={moreInfoPopover}
                           showTitleInfo={props.showTitleInfo}
                           setShowTitleInfo={props.setShowTitleInfo}/>
                <hr/>
                <Card.Text>
                    The sentence in each tab below represents the same 
                    sentence but in different Arabic dialects. The 
                    English translation of the sentence is: 
                </Card.Text>
                <Card.Text className="font-italic text-center pt-2 pb-2">
                    "I’ll take this one, please"
                </Card.Text>
                <Card.Text>
                    See the similarities between the start of MSA 
                    and Tripoli, this overlap between dialects is why 
                    the task of dialect identification can be difficult.
                </Card.Text>
                <Tab.Container defaultActiveKey={dialectExamples[0].key}>
                    <Col>
                        <DialectTabNav data={dialectExamples} />
                    </Col>
                    <Col>
                        <DialectTabContent data={dialectExamples} />
                    </Col>
                </Tab.Container>
            </Card.Body>
        </Col>
    )
}

export default DialectCard;