import TitleContainer  from './TitleContainer'
import LanguageIdentification from './LanguageIdentification';
import SemanticTagging from './SemanticTagging';
import WordCloud from './WordCloud';
import CurrentResearch from './CurrentResearch';
import Contact from './Contact';



const App = () => {

    return (
        <div>
            <TitleContainer />
            <LanguageIdentification />
            <SemanticTagging />
            <WordCloud />
            <CurrentResearch />
            <Contact />
        </div>
    )
}
export default App