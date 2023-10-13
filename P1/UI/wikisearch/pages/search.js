import Head from 'next/head';
import styles from '../styles/Search.module.css';
import { useState } from 'react';
import { getLogin } from '../lib/loginAPI';
import Facet from '../components/Facet';
import FacetTable from '../components/FacetTable'
import DocumentTable from '../components/DocumentTable'
import { getMongo } from '../lib/mongoAPI';
import { getAutonomous } from '../lib/autonomousAPI';
import { useRouter } from 'next/router';

export default function Search() {
    const router = useRouter();
    if (typeof window !== 'undefined') {
        // https://developer.school/snippets/react/localstorage-is-not-defined-nextjs
        // Perform localStorage action
        const login = JSON.parse(localStorage.getItem('login'));
        // if (!login) {
        //     router.push('/index');
        // }
      }

    const [selectedEngine, setSelectedEngine] = useState("MongoAtlas");

    const handleEngineChange = (event) => {
        setSelectedEngine(event.target.value);
    };

    const facetObjectCreate = {
        PageNamespaceFacet: "None",
        PageHasRedirectFacet: "None",
        SiteInfoNameFacet: "None",
        SiteInfoDBNameFacet: "None",
        SiteLanguageFacet: "None",
        PageLastModifiedFacet: "None",
        PageLastModifiedUserFacet: "None",
        PageBytesFacet: "None",
        PageRestrictionsFacet: "None",
        PageNumberLinksFacet: "None"
    };

    const [facetObject, setFacetObject] = useState(facetObjectCreate); 

    function handleFacetChange(event, facet){
        const objectCopy = {...facetObject}
        objectCopy[facet] = event.target.value
        setFacetObject(objectCopy);
        console.log(objectCopy);
    }

    const [facetList, setFacetList] = useState({});
    const [documentList, setDocumentList] = useState([]);

    const [searchInput, setSearchInput] = useState("");
    
    function handleSearchInput(event){
        setSearchInput(event.target.value);
    }

    async function onClickSearch(){
        console.log(searchInput, selectedEngine, facetObject)
        let facetSearch;
        try{
            if (selectedEngine === "MongoAtlas") {
                facetSearch = await getMongo(searchInput, facetObject)
            } else {
                console.log(facetObject)
                facetSearch = await getAutonomous(searchInput, facetObject)
            }
            
        } catch {
            if (selectedEngine === "MongoAtlas") {
                alert("Error connecting to Mongo database.");
            } else {
                alert("Error connecting to Autonomous database.");
            }
            return;
        }
        if (!facetSearch['facets'].length){
                alert("No documents found.");
            } else if (selectedEngine === "MongoAtlas") {
                setFacetList(facetSearch['facets'][0]['facet']);
                setDocumentList(facetSearch['docs']);
            } else{
                if(facetSearch['facets'] !== "123"){
                    const facetOutput = {
                        facet: {}
                    };

                    for (const row of facetSearch['facets']) {
                        const facetCount = row.facetCount;
                        const facetType = row.facetType;
                        const facetValue = row.facetValue;
                        // Revisar que el output este en el facetOutput
                        if (!facetOutput.facet[facetType]) {
                            facetOutput.facet[facetType] = {
                                buckets: []
                            };
                        }
                        // Append the facet value and count to the facet type's bucket
                        facetOutput.facet[facetType].buckets.push({
                            _id: facetValue,
                            count: facetCount
                        });
                    }
                    setFacetList(facetOutput['facet']);
                }
                setDocumentList(facetSearch['docs']);
            }
    }

    function logOut(){
        localStorage.removeItem('login');
        router.push('/');
    }

    return (
        <div className={styles.container}>
            <Head>
                <title>WikiSearch</title>
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <div className={styles.grid}>
                <h1 className={styles.title}>
                    Search
                </h1>
                <div className={styles.middleSection}>
                    <input className={styles.inputT1} type="text" placeholder='Search' onChange={handleSearchInput}/>
                    <button className={styles.searchButton}><img src="/logoBusqueda.svg" onClick={onClickSearch}/></button>
                </div>

                <div>
                    <label className={styles.radioEngine}>
                        <input
                            type="radio"
                            name="radioEngineGroup"
                            value="MongoAtlas"
                            checked={selectedEngine === "MongoAtlas"}
                            onChange={handleEngineChange}
                        />
                        Mongo Atlas
                    </label>

                    <label className={styles.radioEngine}>
                        <input
                            type="radio"
                            name="radioEngineGroup"
                            value="SQL"
                            checked={selectedEngine === "SQL"}
                            onChange={handleEngineChange}
                        />
                        SQL
                    </label>
                </div>

                <div className={styles.contentGrid}>
                    <FacetTable facetList={facetList} facetObject={facetObject} handleFacetChange={handleFacetChange}/>
                    <DocumentTable documentList={documentList} searchQuery={searchInput} searchEngine={selectedEngine}/>
                </div>
                <footer>
                    <button className={styles.logOutButton} onClick={logOut}>Log Out</button>
                    <a
                        href="https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Powered by{' '}
                        <img src="/vercel.svg" alt="Vercel" className={styles.logo} />
                    </a>
                </footer>
            </div>
        </div>
    );
}
