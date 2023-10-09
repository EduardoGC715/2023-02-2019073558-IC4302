import styles from '../styles/Search.module.css';
import { Fragment } from 'react';
import Highlight from './Highlight';

export default function docPreview({ key, doc }){
    
    const pageTitle = typeof doc['PageTitle'] !== 'object' ? doc['PageTitle'] : <Highlight highlight={doc['PageTitle']}/>;
    const pageText = typeof doc['PageText'] !== "undefined" ? 
                            (typeof doc['PageText'] !== 'object' ? doc['PageText'].substring(0,150) : <Highlight highlight={doc['PageText']}/>)
                            : "No title available.";
    const PageLastModified = doc['PageLastModified'] !== null ? 
                            (typeof doc['PageLastModified'] !== 'object' ? doc['PageLastModified'] : <Highlight highlight={doc['PageLastModified']}/>)
                            : "Date not available.";
    const PageLastModifiedUser = typeof doc['PageLastModifiedUser'] !== "undefined" ? 
                            (typeof doc['PageLastModifiedUser'] !== 'object' ? doc['PageLastModifiedUser'] : <Highlight highlight={doc['PageLastModifiedUser']}/>)
                            : "User not available.";
    console.log(PageLastModified, doc['PageLastModified']);
    return <Fragment key={key}>
        <p className={styles.docTitle}>{pageTitle}       </p>
        <p className={styles.normalText}>by {PageLastModifiedUser} on {PageLastModified}</p>
        <p className={styles.pageText}>...{pageText}...</p>
    </Fragment>
}