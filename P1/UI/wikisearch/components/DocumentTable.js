
import styles from '../styles/Search.module.css';
import DocumentPreview from './DocumentPreview';
import { Fragment } from 'react';


export default function DocumentTable({ documentList, searchQuery, searchEngine }) {

    const documentKeys = Object.keys(documentList);
    const documentComponents = documentKeys.map((doc) => <DocumentPreview key={documentList[doc]['_id']} doc={documentList[doc]} searchQuery={searchQuery} searchEngine={searchEngine}/>);
    return (
        <div className={styles.documentList}>
            <p className={styles.facetTitle}>Document List</p>
            {documentComponents}
        </div>
    )
}
