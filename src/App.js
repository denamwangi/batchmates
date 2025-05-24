import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import GraphView from "./GraphView";
import CardView from "./CardView";
import { Route, Routes } from 'react-router-dom';


const API_BASE_URL = "http://127.0.0.1:8080"
function App() {
  const initialGraphData = {
    nodes: [],
    links: [],
  }
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [graphData, setGraphData] = useState(initialGraphData);
  const [peopleInNodes, setPeopleInNodes] = useState(new Set([]))
  const [interestsInNodes, setInterestsInNodes] = useState(new Set([]))
  const location = useLocation()

  const fetchCardViewData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/profiles`);
      const response_json = await response.json();
      response_json["data"].sort((a, b) => a.name.localeCompare(b.name));
      setData(response_json["data"]);
    } catch (e) {
      console.log(e);
    } finally {
      setIsLoading(false);
    }
  };
  const addInterestNode = (interest) => {
    const newNode = [{
      id: interest,
      type: "interest",
      val: 2,
    }];
  
    setGraphData((prev) => ({
      links: [...prev.links],
      nodes: [...prev.nodes, ...newNode],
    }));
    setInterestsInNodes(new Set([...interestsInNodes, interest]))

  }

  const addPersonNode = (person) => {
    const newNode = [{
      id: person,
      type: "person"
    }];
  
    setGraphData((prev) => ({
      links: [...prev.links],
      nodes: [...prev.nodes, ...newNode],
    }));
    setPeopleInNodes(new Set([...peopleInNodes, person]))

  }

useEffect(() => {
  const searchParams = new URLSearchParams(location.search);

  const interest = searchParams.get('interest');
  const person = searchParams.get('person');
  if (interest) {
    const lowerInterest = interest.toLowerCase()
    addInterestNode(lowerInterest)
    fetchPeopleWithInterest(lowerInterest)
    setIsLoading(false)
  } else if (person) {
    addPersonNode(person)
    fetchPersonInterest(person)
    setIsLoading(false)
  } else {
    fetchCardViewData()
  }

}, [location])

  
  const fetchPersonInterest = async (id) => {
    const response = await fetch(
      `${API_BASE_URL}/person/${id}/interests`
    );
    const response_json = await response.json();
    const interests = response_json["data"]["interests"];


    // check if interest exists in nodes already
    const dedupedInterests = [...new Set(interests)];
    console.log('Deduped interests: ', dedupedInterests)
    const newInterests = dedupedInterests.filter(interest => !interestsInNodes.has(interest));
    console.log('interestsInNodes', interestsInNodes)
    console.log('newInterests', newInterests)
    setInterestsInNodes(new Set([...interestsInNodes, ...newInterests]))

    // {'id': 'music', 'type': 'interest', val: 3}
    const newNodes = newInterests.map((interest) => {
      console.log('adding interest: ',interest);
      return {
        id: interest,
        type: "interest",
        val: 2,
      };
    });

    const newLinks = dedupedInterests.map((interest) => ({
      source: id,
      target: interest,
    }));

    console.log("newNodes", newNodes);
    setGraphData((prev) => ({
      links: [...prev.links, ...newLinks],
      nodes: [...prev.nodes, ...newNodes],
    }));
  };


  const fetchPeopleWithInterest = async (interest) => {

    const response = await fetch(
      `${API_BASE_URL}/interest/${interest}/people`
    );
    const response_json = await response.json();
    const people = response_json["data"]["people"];
    console.log("people", people);
    const dedupedPeople = [...new Set(people)];
    const newPeople = dedupedPeople.filter(person => !peopleInNodes.has(person));
    console.log('newPeople:', newPeople)
    console.log('peopleInNodes:', peopleInNodes)
    setPeopleInNodes(new Set([...peopleInNodes, ...newPeople]))

    // {'id': 'music', 'type': 'interest', val: 3}
    const newNodes = newPeople.map((person) => {
      console.log('adding: ', person);
      return {
        id: person,
        type: "person",
      };
    });

    const newLinks = people.map((person) => ({
      source: person,
      target: interest,
    }));

    setGraphData((prev) => ({
      links: [...prev.links, ...newLinks],
      nodes: [...prev.nodes, ...newNodes],
    }));
  }
  
  const handleNodeClick = async (node) => {
    const { id, type } = node;
    console.log("handleNodeClick", id, type);
    if (type === "person") {
      fetchPersonInterest(id)
    } else {
      fetchPeopleWithInterest(id)
    }
  };

  return (
      <Routes>
        <Route
          path="/"
          element={
            <CardView
              isLoading={isLoading}
              data={data}
            />
          }
        />
        <Route
          path="/graph"
          element={
            <GraphView onNodeClick={handleNodeClick} graphData={graphData} isLoading={isLoading} />
          }
        />
      </Routes>
  );
}

export default App;
