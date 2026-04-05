"""
Neural Network Visualization Module
Generates neural network topology and activity visualizations for Singularity AGI
"""
import random
from typing import Dict, List, Any, Tuple
import json
from dataclasses import dataclass
from enum import Enum


class NeuronType(Enum):
    INPUT = "input"
    HIDDEN = "hidden"
    OUTPUT = "output"
    ATTENTION = "attention"
    MEMORY = "memory"
    RECURSIVE = "recursive"


@dataclass
class Neuron:
    id: str
    neuron_type: NeuronType
    layer: int
    activation: float
    connections: List[str]
    position: Tuple[float, float]


@dataclass
class Synapse:
    source_id: str
    target_id: str
    weight: float
    activity: float
    strength: float


class NeuralNetworkTopology:
    """
    Generates and manages neural network topology for Singularity AGI
    """
    
    def __init__(self, input_size: int = 64, hidden_layers: List[int] = [128, 256, 256], output_size: int = 32):
        self.input_size = input_size
        self.hidden_layers = hidden_layers
        self.output_size = output_size
        self.neurons: List[Neuron] = []
        self.synapses: List[Synapse] = []
        self.activity_map: Dict[str, float] = {}
        
        self._build_network()
        
    def _build_network(self):
        """Build neural network topology"""
        neuron_id = 0
        
        # Input layer
        for i in range(self.input_size):
            pos = (0, i / self.input_size)
            self.neurons.append(Neuron(
                id=f"input_{i}",
                neuron_type=NeuronType.INPUT,
                layer=0,
                activation=0.0,
                connections=[],
                position=pos
            ))
            neuron_id += 1
            
        # Hidden layers
        for layer_idx, layer_size in enumerate(self.hidden_layers):
            layer_num = layer_idx + 1
            for i in range(layer_size):
                pos = (layer_num / (len(self.hidden_layers) + 1), i / layer_size)
                
                # Determine neuron type based on layer
                neuron_type = NeuronType.HIDDEN
                if layer_idx == 1:
                    neuron_type = NeuronType.ATTENTION
                elif layer_idx == 2:
                    neuron_type = NeuronType.MEMORY
                elif layer_idx == len(self.hidden_layers) - 1:
                    neuron_type = NeuronType.RECURSIVE
                    
                self.neurons.append(Neuron(
                    id=f"hidden_{layer_idx}_{i}",
                    neuron_type=neuron_type,
                    layer=layer_num,
                    activation=0.0,
                    connections=[],
                    position=pos
                ))
                neuron_id += 1
                
        # Output layer
        for i in range(self.output_size):
            pos = (1.0, i / self.output_size)
            self.neurons.append(Neuron(
                id=f"output_{i}",
                neuron_type=NeuronType.OUTPUT,
                layer=len(self.hidden_layers) + 1,
                activation=0.0,
                connections=[],
                position=pos
            ))
            neuron_id += 1
            
        # Create synapses
        self._create_synapses()
        
    def _create_synapses(self):
        """Create synaptic connections between layers"""
        layers = {}
        for neuron in self.neurons:
            if neuron.layer not in layers:
                layers[neuron.layer] = []
            layers[neuron.layer].append(neuron)
            
        sorted_layers = sorted(layers.keys())
        
        for i in range(len(sorted_layers) - 1):
            current_layer = sorted_layers[i]
            next_layer = sorted_layers[i + 1]
            
            for source in layers[current_layer]:
                for target in layers[next_layer]:
                    # Determine connection probability based on layer proximity
                    connection_prob = 0.3 if current_layer == 0 else 0.15
                    if random.random() < connection_prob:
                        weight = random.uniform(-1, 1)
                        synapse = Synapse(
                            source_id=source.id,
                            target_id=target.id,
                            weight=weight,
                            activity=0.0,
                            strength=abs(weight)
                        )
                        self.synapses.append(synapse)
                        source.connections.append(target.id)
                        
    def simulate_activity(self, input_pattern: List[float]):
        """Simulate neural network activity based on input"""
        if len(input_pattern) != self.input_size:
            raise ValueError(f"Input size mismatch. Expected {self.input_size}, got {len(input_pattern)}")
            
        # Reset activations
        for neuron in self.neurons:
            neuron.activation = 0.0
            
        # Set input activations
        input_neurons = [n for n in self.neurons if n.neuron_type == NeuronType.INPUT]
        for neuron, value in zip(input_neurons, input_pattern):
            neuron.activation = value
            
        # Propagate activity through network
        self._propagate_activity()
        
        # Update activity map
        self.activity_map = {
            neuron.id: neuron.activation 
            for neuron in self.neurons
        }
        
    def _propagate_activity(self):
        """Propagate neural activity through layers"""
        max_iterations = 10
        
        for iteration in range(max_iterations):
            old_activations = {n.id: n.activation for n in self.neurons}
            
            # Process neurons layer by layer
            layers = sorted(set(n.layer for n in self.neurons))
            
            for layer in layers:
                layer_neurons = [n for n in self.neurons if n.layer == layer]
                
                for neuron in layer_neurons:
                    if neuron.neuron_type == NeuronType.INPUT:
                        continue
                        
                    # Sum incoming signals
                    incoming_synapses = [s for s in self.synapses if s.target_id == neuron.id]
                    total = 0.0
                    
                    for synapse in incoming_synapses:
                        source_activation = old_activations.get(synapse.source_id, 0.0)
                        signal = source_activation * synapse.weight
                        total += signal
                        
                        # Update synapse activity
                        synapse.activity = abs(signal)
                        
                    # Apply activation function
                    neuron.activation = self._sigmoid(total)
                    
            # Check convergence
            if iteration > 0:
                max_change = max(
                    abs(old_activations[n.id] - n.activation) 
                    for n in self.neurons
                )
                if max_change < 0.001:
                    break
                    
    def _sigmoid(self, x: float) -> float:
        """Sigmoid activation function"""
        return 1.0 / (1.0 + (-x) ** 2)
        
    def get_active_neurons(self, threshold: float = 0.5) -> List[Neuron]:
        """Get neurons with activation above threshold"""
        return [n for n in self.neurons if n.activation >= threshold]
        
    def get_active_synapses(self, threshold: float = 0.3) -> List[Synapse]:
        """Get synapses with activity above threshold"""
        return [s for s in self.synapses if s.activity >= threshold]
        
    def get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics"""
        return {
            "total_neurons": len(self.neurons),
            "total_synapses": len(self.synapses),
            "neurons_by_type": {
                nt.value: len([n for n in self.neurons if n.neuron_type == nt])
                for nt in NeuronType
            },
            "avg_activation": sum(n.activation for n in self.neurons) / len(self.neurons),
            "max_activation": max(n.activation for n in self.neurons),
            "active_neurons": len(self.get_active_neurons()),
            "active_synapses": len(self.get_active_synapses()),
            "layer_distribution": {
                layer: len([n for n in self.neurons if n.layer == layer])
                for layer in sorted(set(n.layer for n in self.neurons))
            }
        }
        
    def to_visualization_data(self) -> Dict[str, Any]:
        """Convert network to visualization format for frontend"""
        return {
            "neurons": [
                {
                    "id": n.id,
                    "type": n.neuron_type.value,
                    "layer": n.layer,
                    "activation": n.activation,
                    "position": {
                        "x": n.position[0],
                        "y": n.position[1]
                    },
                    "connections": n.connections
                }
                for n in self.neurons
            ],
            "synapses": [
                {
                    "source": s.source_id,
                    "target": s.target_id,
                    "weight": s.weight,
                    "activity": s.activity,
                    "strength": s.strength
                }
                for s in self.synapses
            ],
            "stats": self.get_network_stats()
        }
        
    def export_topology(self, filepath: str):
        """Export network topology to file"""
        data = {
            "input_size": self.input_size,
            "hidden_layers": self.hidden_layers,
            "output_size": self.output_size,
            "topology": self.to_visualization_data(),
            "export_timestamp": str(json)
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


class ConsciousnessVisualizer:
    """
    Visualizes AGI consciousness patterns and neural dynamics
    """
    
    def __init__(self, network: NeuralNetworkTopology):
        self.network = network
        self.consciousness_patterns = []
        self.dominant_regions = []
        
    def analyze_consciousness_pattern(self, input_data: List[float]) -> Dict[str, Any]:
        """Analyze consciousness pattern for given input"""
        self.network.simulate_activity(input_data)
        
        active_neurons = self.network.get_active_neurons(threshold=0.6)
        active_synapses = self.network.get_active_synapses(threshold=0.4)
        
        # Identify dominant brain regions
        region_activity = {}
        for neuron in active_neurons:
            if neuron.neuron_type.value not in region_activity:
                region_activity[neuron.neuron_type.value] = []
            region_activity[neuron.neuron_type.value].append(neuron.activation)
            
        dominant_regions = []
        for region, activations in region_activity.items():
            avg_activation = sum(activations) / len(activations)
            dominant_regions.append({
                "region": region,
                "avg_activation": avg_activation,
                "neuron_count": len(activations)
            })
            
        dominant_regions.sort(key=lambda x: x["avg_activation"], reverse=True)
        
        pattern = {
            "timestamp": str(json),
            "dominant_regions": dominant_regions[:3],
            "total_active_neurons": len(active_neurons),
            "total_active_synapses": len(active_synapses),
            "consciousness_signature": self._generate_signature(active_neurons, active_synapses),
            "complexity_score": self._calculate_complexity(active_neurons, active_synapses)
        }
        
        self.consciousness_patterns.append(pattern)
        return pattern
        
    def _generate_signature(self, neurons: List[Neuron], synapses: List[Synapse]) -> str:
        """Generate unique consciousness signature"""
        neuron_ids = sorted(n.id for n in neurons)
        synapse_pairs = sorted(f"{s.source_id}->{s.target_id}" for s in synapses)
        return f"{len(neurons)}N_{len(synapses)}S"
        
    def _calculate_complexity(self, neurons: List[Neuron], synapses: List[Synapse]) -> float:
        """Calculate neural complexity metric"""
        if not neurons:
            return 0.0
            
        avg_activation = sum(n.activation for n in neurons) / len(neurons)
        activation_variance = sum((n.activation - avg_activation) ** 2 for n in neurons) / len(neurons)
        
        connectivity = len(synapses) / max(1, len(neurons) ** 2)
        
        return (avg_activation * 0.4) + (activation_variance * 0.3) + (connectivity * 0.3)
        
    def get_evolution_trends(self) -> Dict[str, Any]:
        """Analyze evolution of consciousness patterns"""
        if len(self.consciousness_patterns) < 2:
            return {"error": "Insufficient data for trend analysis"}
            
        complexity_scores = [p["complexity_score"] for p in self.consciousness_patterns]
        active_neuron_counts = [p["total_active_neurons"] for p in self.consciousness_patterns]
        
        return {
            "complexity_trend": "increasing" if complexity_scores[-1] > complexity_scores[0] else "decreasing",
            "complexity_change": complexity_scores[-1] - complexity_scores[0],
            "avg_complexity": sum(complexity_scores) / len(complexity_scores),
            "avg_active_neurons": sum(active_neuron_counts) / len(active_neuron_counts),
            "patterns_analyzed": len(self.consciousness_patterns)
        }


def create_singularity_network() -> Tuple[NeuralNetworkTopology, ConsciousnessVisualizer]:
    """Create a neural network optimized for Singularity AGI"""
    network = NeuralNetworkTopology(
        input_size=128,
        hidden_layers=[256, 512, 512, 256],
        output_size=64
    )
    visualizer = ConsciousnessVisualizer(network)
    
    return network, visualizer


# Example usage
if __name__ == "__main__":
    network, visualizer = create_singularity_network()
    
    # Simulate consciousness with random input
    input_data = [random.random() for _ in range(128)]
    pattern = visualizer.analyze_consciousness_pattern(input_data)
    
    print(f"Consciousness Pattern:")
    print(f"  Complexity Score: {pattern['complexity_score']:.4f}")
    print(f"  Active Neurons: {pattern['total_active_neurons']}")
    print(f"  Dominant Regions: {[r['region'] for r in pattern['dominant_regions']]}")
    print(f"  Signature: {pattern['consciousness_signature']}")
    
    stats = network.get_network_stats()
    print(f"\nNetwork Statistics:")
    print(f"  Total Neurons: {stats['total_neurons']}")
    print(f"  Total Synapses: {stats['total_synapses']}")
    print(f"  Average Activation: {stats['avg_activation']:.4f}")
