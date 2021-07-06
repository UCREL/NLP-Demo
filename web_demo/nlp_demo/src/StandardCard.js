import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';

import { CardLabel, InfoTitle } from './CardUtilities';

const moreInfoPopover = (
    [<div key="1">
        <p>
            The main researcher at Lancaster that conducts dialect identification
            research is <a href="https://www.lancaster.ac.uk/staff/elhaj/index.html">
            Dr. Mahmoud El-Haj</a>. 
        </p>
        <p>
            <a href="https://www.lancaster.ac.uk/staff/elhaj/docs/habibi.pdf">In 
            his latest work on dialect identification 
            he created a novel dataset from Arabic song lyrics that covered 6 
            Arabic dialects from 18 Arabic Countries, and benchmarked various 
            machine learning models on this new dataset</a>.
        </p>
    </div>]
);

const StandardCard = (props) => {

    return (
        <Col xs={12} lg={{span: 10, offset: 1}}>
            <Card.Body>
                <InfoTitle title="Standard" info={moreInfoPopover}
                           showTitleInfo={props.showTitleInfo}
                           setShowTitleInfo={props.setShowTitleInfo} />
                <hr/>
            </Card.Body>
            <CardLabel text="Lancaster uni has a yearly competition with York Uni, 
                    the roses tournament." label="English"/>
            <Card.Body>
                <p>
                    At Lancaster we conduct research into dialect identification
                    a similar task to language identification (see the dialects tab above).
                    For more information on the academic papers that have been written on 
                    this topic from researchers at Lancaster click the information image 
                    in the top right hand corner of this box (
                    <i className="bi bi-info-circle" role="img" 
                    aria-label="Information image example"/>).
                </p>
            </Card.Body>
        </Col>
    )
}

export default StandardCard;