import styles from '../styles/Search.module.css';
import { Fragment } from 'react';
import Highlight from './Highlight';
import Link from 'next/link'

export default function docPreviewAutonomous({ key, doc, searchQuery, searchEngine }){
    
    console.log(doc);
    const pageTitle = typeof doc['pageTitle'] !== 'undefined' ? doc['pageTitle'] : "No title available.";

    const pageText = typeof doc['pageText'] !== "undefined" ? doc['pageText'].substring(0,150) : "No text available.";

    const PageLastModified = doc['pageLastModified'] !== null ? doc['pageLastModified'] : "Date not available.";

    const PageLastModifiedUser = typeof doc['pageLastModifiedUser'] !== "undefined" ? doc['pageLastModifiedUser'] : "User not available.";

    const PageBytes = typeof doc['pageBytes'] !== "undefined" ? doc['pageBytes'] : "Bytes not available.";
   
    const PageRedirect = typeof doc['pageRedirect'] !== "undefined" && doc['pageRedirect'] !== null ? doc['pageRedirect'] : "No redirect available.";
   
    const PageNamespace = doc['pageNamespace'] !== null ? doc['pageNamespace'] : "Date not available.";

    let PageLinks;
    if (typeof doc['pageLinks'] === 'string' && doc['pageLinks'].trim() !== '') { // check if PageLinks is a non-empty string

        const linksArray = doc['pageLinks'].split(','); // Split the string into an array based on commas

        // Map the links and wrap each in a span
        PageLinks = linksArray.map((link) => {
            return <span className={styles.normalText}><br />- {link.trim()}</span> // Trim to remove any extra whitespace
        });
    } else {
        PageLinks = "No links available."
    }

    //console.log(PageLastModified, doc['PageLastModified']);
    return <Fragment key={key}>
        <Link href={{pathname: '/docView', query:{id: doc['pageId'], searchQuery, searchEngine}}}><p className={styles.docTitle}>{pageTitle}</p></Link>
        <p className={styles.normalText}>by {PageLastModifiedUser} on {PageLastModified}</p>
        <p className={styles.pageText}>...{pageText}...</p>
        <p className={styles.normalText}>Redirect: {PageRedirect}</p>
        <p className={styles.normalText}>Namespace: {PageNamespace} Bytes: {PageBytes}<br />PageLinks: {PageLinks}</p>
    </Fragment>
}