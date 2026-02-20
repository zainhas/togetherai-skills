#!/usr/bin/env python3
"""
Together AI Fine-Tuning — Full Workflow (v2 SDK)

End-to-end: prepare data → upload → create job → monitor → deploy.

Usage:
    python finetune_workflow.py

Requires:
    pip install together
    export TOGETHER_API_KEY=your_key
"""

import json
import time
import tempfile
from together import Together

client = Together()

# --- 1. Prepare training data (conversational format) ---
training_data = [
    {
        "messages": [
            {"role": "system", "content": "You are a helpful customer support agent."},
            {"role": "user", "content": "How do I reset my password?"},
            {"role": "assistant", "content": "Go to Settings > Security > Reset Password. You'll receive a confirmation email within 5 minutes."},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "You are a helpful customer support agent."},
            {"role": "user", "content": "What are your business hours?"},
            {"role": "assistant", "content": "We're available Monday-Friday, 9 AM - 6 PM EST. Weekend support is available via email."},
        ]
    },
    # Add more training examples...
]

data_path = tempfile.mktemp(suffix=".jsonl")
with open(data_path, "w") as f:
    for example in training_data:
        f.write(json.dumps(example) + "\n")

print(f"Wrote {len(training_data)} examples to {data_path}")

# --- 2. Upload training file ---
file_response = client.files.upload(file=data_path, purpose="fine-tune", check=True)
file_id = file_response.id
print(f"Uploaded file: {file_id}")

# --- 3. Create fine-tuning job ---
job = client.fine_tuning.create(
    training_file=file_id,
    model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    n_epochs=3,
    learning_rate=1e-5,
    lora=True,
    suffix="my-custom-model",
)
print(f"Created fine-tuning job: {job.id}")

# --- 4. Monitor training ---
while True:
    status = client.fine_tuning.retrieve(id=job.id)
    print(f"  Status: {status.status}")

    if status.status == "completed":
        print(f"\nTraining complete!")
        print(f"  Output model: {status.output_name}")
        break
    elif status.status in ("failed", "cancelled"):
        print(f"Job ended: {status.status}")
        exit(1)

    time.sleep(30)

# --- 5. List training events ---
events = client.fine_tuning.list_events(id=job.id)
for event in events.data:
    print(f"  [{event.created_at}] {event.message}")

# --- 6. Use the fine-tuned model (Serverless LoRA) ---
output_model = status.output_name
response = client.chat.completions.create(
    model=output_model,
    messages=[
        {"role": "system", "content": "You are a helpful customer support agent."},
        {"role": "user", "content": "How do I update my billing info?"},
    ],
)
print(f"\nFine-tuned model response: {response.choices[0].message.content}")
