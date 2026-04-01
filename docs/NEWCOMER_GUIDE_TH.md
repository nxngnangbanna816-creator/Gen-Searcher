# คู่มือผู้มาใหม่ (Gen-Searcher)

เอกสารนี้สรุปภาพรวมโครงสร้าง repo สำหรับคนที่เพิ่งเริ่มต้น เพื่อให้หาโค้ดได้เร็วและรู้ว่าควรเริ่มอ่านตรงไหนก่อน

> เวอร์ชันหน้าเว็บ HTML: `docs/NEWCOMER_GUIDE_TH.html`

## 1) โครงสร้างระดับบนของ repository

โปรเจกต์นี้แบ่งเป็น 4 ส่วนหลัก:

- `Gen-DeepResearch-SFT/` — ส่วน Supervised Fine-Tuning (SFT) โดยวางบน LLaMA-Factory
- `Gen-DeepResearch-RL/` — ส่วน Reinforcement Learning (RL) และ workflow ของ agentic deep research
- `qwen_image_api_server/` — บริการ FastAPI สำหรับเรียก image generator (เช่น Qwen-Image-Edit)
- `KnowGen_Eval/` — สคริปต์ประเมินผล benchmark (GPT-based evaluation)

โฟลเดอร์ `assets/` และ `README.md` ใช้สำหรับสื่ออธิบายงานและวิธีใช้งานระดับภาพรวม

## 2) ส่วนที่สำคัญและหน้าที่ของแต่ละโฟลเดอร์

### A) `README.md` (root)
- อธิบายภาพรวมโปรเจกต์, ลิงก์โมเดล/ดาต้า, ขั้นตอน train/inference/eval แบบ end-to-end
- เป็นจุดเริ่มต้นที่ควรอ่านก่อนเสมอ

### B) `Gen-DeepResearch-SFT/LLaMA-Factory/`
- ใช้สำหรับฝั่ง SFT เพื่อฝึกโมเดลฐานให้มีพฤติกรรมตามที่ต้องการก่อนเข้า RL
- ใน README หลักมีตัวอย่างคำสั่ง `llamafactory-cli train ...` ที่ชี้ไปยังส่วนนี้

### C) `Gen-DeepResearch-RL/rllm/`
- เป็นแกนของฝั่ง RL workflow
- README หลักระบุว่าต้องติดตั้ง `verl` และ `rllm` จากส่วนนี้ก่อนเริ่มเทรน RL
- ภายในมี workflow สำหรับ agentic search/browse/reason ก่อนสร้างภาพ

### D) `qwen_image_api_server/`
- ทำหน้าที่เสิร์ฟ image generation model ผ่าน API
- RL rollout/inference เรียก endpoint จากบริการนี้
- จุดแก้โมเดลสร้างภาพอยู่ที่ `qwen_image_api_server/qwen-image-edit/api.py`

### E) `KnowGen_Eval/`
- รวมสคริปต์ประเมินผล benchmark
- `gpt_eval_knowgen.py` อ่านผลลัพธ์ที่มี `prompt`, `output_path`, `gt_image` แล้วเรียกโมเดลภายนอกให้ให้คะแนนเชิงคุณภาพ

## 3) ภาพการไหลของระบบ (mental model)

ลำดับการทำงานแบบสั้น:
1. เตรียม environment + dataset
2. ฝึก SFT model
3. ตั้งค่าเครื่องมือภายนอก (search/browse/image generation services)
4. ฝึก RL ให้ agent ใช้เครื่องมือเพื่อหา evidence
5. รัน inference เพื่อสร้างผลลัพธ์ grounded results + ภาพ
6. รัน KnowGen evaluation เพื่อสรุปคะแนน

## 4) สิ่งสำคัญที่ผู้มาใหม่ต้องรู้

1. **Repo นี้เป็น multi-component repo**
   - ต้องเข้าใจว่า SFT, RL, API server, Eval แยกกันชัดเจน แต่พึ่งพากัน

2. **Dependency สูงและใช้ทรัพยากรเยอะ**
   - ใน README ระบุความต้องการ GPU ระดับหลายใบ (80GB) สำหรับ SFT/RL

3. **มี external services/key หลายตัว**
   - เช่น search service, browse summary model endpoint, image API endpoint, และ API keys
   - ถ้า service ใดไม่ขึ้น ระบบปลายทางจะรันไม่ครบ

4. **การประเมินผลแยกจากการเทรน**
   - `KnowGen_Eval` ใช้ข้อมูลผลลัพธ์จากขั้น inference ดังนั้น path และ format JSON ต้องสอดคล้อง

5. **หลายส่วนเป็น sub-project จาก upstream**
   - เช่น LLaMA-Factory, rLLM, Megatron-LM
   - เวลาปรับแก้ต้องระวังผลกระทบและความเข้ากันของเวอร์ชัน

## 5) แผนการเรียนรู้ต่อ (แนะนำเป็นลำดับ)

### ระยะที่ 1: เข้าใจภาพรวมก่อน (1–2 วัน)
- อ่าน `README.md` ทั้งไฟล์
- วาด flow จาก SFT → RL → Inference → Eval ด้วยคำของตัวเอง

### ระยะที่ 2: ลงลึกเฉพาะทาง RL workflow (2–4 วัน)
- อ่านเอกสาร/สคริปต์ใน `Gen-DeepResearch-RL/rllm/vision_deepresearch_async_workflow/`
- ทำความเข้าใจว่ามี tools อะไร, เรียกใช้ตอนไหน, reward มาจากไหน

### ระยะที่ 3: เข้าใจ data contract (1–2 วัน)
- ตรวจ JSON format ที่ train/inference/eval ใช้ร่วมกัน
- ทำ checklist ช่องที่ต้องมี (id, prompt, output_path, gt_image, meta ฯลฯ)

### ระยะที่ 4: ลองรันแบบเล็ก (sandbox run)
- เริ่มจาก inference/eval บนชุดข้อมูลจำนวนน้อย
- ยืนยันว่า endpoint และ key ทำงานครบก่อนค่อย scale

### ระยะที่ 5: ค่อยปรับแต่งเชิงวิจัย
- ปรับ prompt/tool config/reward function ทีละตัว
- วัดผลด้วย benchmark เดิม เพื่อแยกผลของแต่ละการเปลี่ยนแปลง

## 6) จุดเริ่มปฏิบัติจริง (quick checklist)

- [ ] อ่าน root `README.md`
- [ ] ยืนยัน environment ของ SFT และ RL แยกกัน
- [ ] ตั้งค่า `.env.gen_image` และ endpoint ให้ครบ
- [ ] ทดสอบ image API server แยกเดี่ยวก่อน
- [ ] รัน inference ตัวอย่างเล็ก
- [ ] รัน `KnowGen_Eval` และตรวจ output JSON ว่าครบ

---

ถ้าเริ่มต้นครั้งแรก ให้โฟกัส “รันให้ครบหนึ่งรอบเล็ก ๆ” ก่อน optimization เสมอ เพราะจะเห็นภาพ dependency ของระบบทั้งหมดเร็วที่สุด

## 7) ตัวอย่างเครื่องมือ + ทดสอบระบบอย่างเร็ว

เพิ่มเครื่องมือตัวอย่าง `sample_tool` ที่รับข้อความแล้วคืนค่า word/character count เพื่อใช้ smoke test pipeline ของ tools

รันทดสอบ:

```bash
cd Gen-DeepResearch-RL/rllm
PYTHONPATH=. python vision_deepresearch_async_workflow/tools/test_sample_tool.py
```

ถ้าผ่านจะเห็นข้อความ `sample_tool test passed`
