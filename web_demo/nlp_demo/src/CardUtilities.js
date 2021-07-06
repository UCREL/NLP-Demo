import './_card.scss';
import './index.scss';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Popover from 'react-bootstrap/Popover';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

const infoPopover = (info) => {
    return (
        <Popover>
            <Popover.Content> 
                {info}
            </Popover.Content>
        </Popover>
    )
}


const TranslationText = (props) => {

    if (typeof props.translation !== 'undefined') {
        return (
            <div className="flex-wrap flex-space-evenly" 
                 style={{width: "100%", "alignItems": "center"}}>
                <p className="m-1">{props.text}</p>
                <OverlayTrigger placement="bottom"
                                show={props.showTranslationText} 
                                overlay={infoPopover(props.translation)}>
                    <Button onClick={() => {props.setShowTranslationText(!props.showTranslationText)}}
                            className="m-1 bold">
                        Translation
                    </Button> 
                </OverlayTrigger>
            </div>
        )
    }
    else {
        return <p>{props.text}</p>
    }

}

const InfoTitle = (props) => {
    const popover = infoPopover(props.info);
    return (
        <div className="flex">
            <Card.Title className="text-center flex-grow-1" 
                        style={{paddingLeft: "1rem"}}>
                <h3>{props.title}</h3>
            </Card.Title>
            <OverlayTrigger placement="left" overlay={popover} 
                            show={props.showTitleInfo} 
                            >
                <i className="bi bi-info-circle cursor-pointer" role="img" 
                   aria-label="Information" 
                   onClick={() => {props.setShowTitleInfo(!props.showTitleInfo)}}/>
            </OverlayTrigger>
        </div>
    )
}

const CardLabel = (props) => {
    return (
        <Container className="card-label-container">
            <Row>
                <Col className="card-label-names card-label-col" 
                    sm={4} md={{ span: 3, offset: 1 }}>
                    <h4>Input</h4>
                </Col>
                <Col sm={8} md={{ span: 7}} 
                     className="card-label-col card-label-input-value">
                    <TranslationText showTranslationText={props.showTranslationText} 
                                     setShowTranslationText={props.setShowTranslationText}
                                     text={props.text} translation={props.translation}/>
                </Col>
            </Row>
            <Row>
                <Col className="card-label-names card-label-col" 
                    sm={4} md={{ span: 3, offset: 1 }} >
                    <h4>Output</h4>
                </Col>
                <Col className="card-label-output-value card-label-col" 
                    sm={8} md={{ span: 7}} >
                    <h4>
                        {props.label}
                    </h4>
                </Col>
            </Row>
        </Container>
    )
}

export { CardLabel, InfoTitle };