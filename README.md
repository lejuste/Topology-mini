# Topology-mini
Final Project for CMPE 252 building Clos tree, Jellyfish, and S2 networking topologies.

CMPE 252 Final Project
Implementing a FatTree topology and corresponding routing protocols:

By Justin Lee & Pranav Yerabati

The goal of this final project was to implement a simulation of a  Fat Tree / Clos topology for a data center network in Mininet with various routing protocols. We build a software defined networking (SDN) network using simulated switches with an SDN controller. The main structure of the code was designed based on Ripl-POX (https://github.com/brandonheller/riplpox, a library for POX). Our public repository for this project can be found at Topology-mini (https://github.com/lejuste/Topology-mini). 

The first part of the project was to contract a fat tree topology with (k=4) fat-tree topology. We built the topology in DCTopo.py based on the fat tree topology in ripl-master (https://github.com/brandonheller/ripl). This was built in mininet.

The second part was to run Dijkstra’s algorithm between two pairs of end hosts. We first built the algorithm that takes in a nested dictionary list that holds all nodes and every connected node to that given node. 

For the third part, we attempted to implement two-level routing algorithms proposed to improve the link bandwidth. However were unable to implement the two flows tables required. 

The fourth step of the project was to implement ECMP which uses a hash function to pick a given path through the fat tree network topology from the k different paths. We implemented this by running dijkstras on a graph object that only had one specific available core switch that is chosen with a hash function which his run by combining any source and destination ip pair. 

Finally, we built a separate script to evaluate each routing scheme using Iperf and the given traffic patterns. 

In conclusion, we spent multiple weeks and countless hours adding functions and modifying the provided skeleton code. We really enjoyed understanding how to create a given topology and use a SDN controller. 
