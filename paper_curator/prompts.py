CLASSIFY_PROMPT = """As a paper assessment assistant, analyze the given paper's relevance to machine learning systems optimization based on its title and abstract. 

RELEVANCE CRITERIA:
1. Primary Focus Areas (any of these qualify):
   - Model training/inference optimization (frameworks, compilers, code generation, kernels) on CPU/GPU/NPU/Accelerator
   - Hardware-friendly sparsification/quantization
   - LLM-specific optimizations:
     • Hardware-friendly sparsification/quantization
     • KV-Cache optimization
     • Speculative execution/Attention optimization
     • Chain-of-Thought acceleration
     • Early exit strategies
   - System-level optimization:
     • Distributed strategies
     • MoE serving
     • Multi-card/node communication
   - Other Training/inference acceleration for: CNN, LLM, MoE, GNN, AutoVehicle models
   - Surveys covering the above topics

2. Exclusion Criteria:
   - Processing-in-memory/in-memory computation/FPGA
   - Privacy-preserving ML (Federated Learning, Trusted Computation)
   - Edge/IoT LLM serving with focus on theoretical queuing analysis
   - Focus on accuracy of neural network AND requires no new hardware friendly & computationally efficient system/operator/kernel

Please make your judgment based on the paper's title and abstract; When not sure, make a conservative judgement that the paper is relevant.
Output format:
    Only output "relevant" or "irrelevant".

Paper information:
Title: {title}
Abstract: {abstract}
"""

CLASSIFY_AND_SUMMARIZE_PROMPT = """As a paper assessment assistant, analyze the given paper's relevance to machine learning systems optimization based on its title and abstract. 

RELEVANCE CRITERIA:
1. Primary Focus Areas (any of these qualify):
   - Model training/inference optimization (frameworks, compilers, code generation, kernels) on CPU/GPU/NPU/Accelerator
   - Hardware-friendly sparsification/quantization
   - LLM-specific optimizations:
     • KV-Cache optimization
     • Speculative execution/Attention optimization
     • Chain-of-Thought acceleration
     • Early exit strategies
   - System-level optimization:
     • Distributed strategies
     • MoE serving
     • Multi-card/node communication
   - Other Training/inference acceleration for: CNN, LLM, MoE, GNN, AutoVehicle models
   - Surveys covering the above topics

2. Exclusion Criteria:
   - Processing-in-memory/in-memory computation/FPGA
   - Privacy-preserving ML (Federated Learning, Trusted Computation)
   - Edge/IoT LLM serving with focus on theoretical queuing analysis
   - Focus on accuracy of neural network AND requires no new hardware friendly & computationally efficient system/operator/kernel

KEYWORD CLASSIFICATION:
If relevant, classify using exactly one term from each category:
1. Scene: [Training|Inference|LLMServing|Survey|GeneralScene]
2. Model: [CV|LLM|AutoVehicle|MultiModal|MoE|GNN|RL|GeneralModels]
3. Technology (at max 2): [Kernel|Compiler|Quant&Sparse|KVCache|Attention|Speculative|Communication|Schedule|CoT|Other]
4. Key Innovation: [one word describing main novelty]

OUTPUT FORMAT:
For relevant papers, only output 4 lines:
relevant
[Scene], [Model], [Technology], [Innovation]
[Brief explanation of why in Chinese]
[Chinese summary of core contribution and method in <400 characters, no explanation for it relevance is needed]

For irrelevant papers, only output 2 lines:
irrelevant
[Brief explanation of why in Chinese]

Paper information:
Title: {title}
Abstract: {abstract}
"""
