import { api } from "../config/api";

export async function analyzeImage(question, file) {
  const fd = new FormData();
  fd.append("question", question);
  fd.append("image", file);

  try {
    const res = await api.post("/analyze", fd);
    return res.data;
  } catch (error) {
    console.error("Analyze failed", error);
    if (error.response.status === 422) {
      throw new Error(error.response.data.detail);
    }
    throw new Error(`Analyze failed (${error.response.status})`);
  }
}

export async function readMileage(file) {
  const fd = new FormData();
  fd.append("image", file);

  try {
    const res = await api.post("/read_mileage", fd);
    return res.data;
  } catch (error) {
    console.error("Read mileage failed", error);
    if (error.response.status === 422) {
      throw new Error(error.response.data.detail);
    }
    throw new Error(`Read mileage failed (${error.response.status})`);
  }
}

export async function readVIN(file) {
  const fd = new FormData();
  fd.append("image", file);

  try {
    const res = await api.post("/read_vin", fd);
    return res.data;
  } catch (error) {
    console.error("Read VIN failed", error);
    if (error.response.status === 422) {
      throw new Error(error.response.data.detail);
    }
    throw new Error(`Read VIN failed (${error.response.status})`);
  }
}
