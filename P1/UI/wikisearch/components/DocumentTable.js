
import styles from '../styles/Search.module.css';
import DocumentPreview from './DocumentPreview';
import DocumentPreviewAutonomous from './DocumentPreviewAutonomous';
import { Fragment } from 'react';


export default function DocumentTable({ documentList, searchQuery, searchEngine }) {

    const documentKeys = Object.keys(documentList);
    let documentComponents;
    if(searchEngine === "SQL"){
        documentComponents = documentKeys.map((doc) => <DocumentPreviewAutonomous key={documentList[doc]['pageId']} doc={documentList[doc]} searchQuery={searchQuery} searchEngine={searchEngine}/>);

    }else {
        documentComponents = documentKeys.map((doc) => <DocumentPreview key={documentList[doc]['_id']} doc={documentList[doc]} searchQuery={searchQuery} searchEngine={searchEngine}/>);

    }
    return (
        <div className={styles.documentList}>
            <p className={styles.facetTitle}>Document List</p>
            {documentComponents}
        </div>
    )

}
