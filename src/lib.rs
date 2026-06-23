use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub enum InfraState {
    Idle,
    Planning,
    Approved,
    Executing,
    Success,
    Failed,
}

impl InfraState {
    fn from_str(state: &str) -> Option<Self> {
        match state {
            "Idle" => Some(InfraState::Idle),
            "Planning" => Some(InfraState::Planning),
            "Approved" => Some(InfraState::Approved),
            "Executing" => Some(InfraState::Executing),
            "Success" => Some(InfraState::Success),
            "Failed" => Some(InfraState::Failed),
            _ => None,
        }
    }

    fn as_str(&self) -> &str {
        match self {
            InfraState::Idle => "Idle",
            InfraState::Planning => "Planning",
            InfraState::Approved => "Approved",
            InfraState::Executing => "Executing",
            InfraState::Success => "Success",
            InfraState::Failed => "Failed",
        }
    }
}

#[pyclass]
pub struct StateMachine {
    current_state: InfraState,
    allowed_transitions: HashMap<String, Vec<String>>,
}

#[pymethods]
impl StateMachine {
    #[new]
    fn new() -> Self {
        let mut transitions = HashMap::new();
        transitions.insert("Idle".to_string(), vec!["Planning".to_string()]);
        transitions.insert("Planning".to_string(), vec!["Approved".to_string(), "Failed".to_string()]);
        transitions.insert("Approved".to_string(), vec!["Executing".to_string(), "Failed".to_string()]);
        transitions.insert("Executing".to_string(), vec!["Success".to_string(), "Failed".to_string()]);
        transitions.insert("Success".to_string(), vec!["Idle".to_string()]);
        transitions.insert("Failed".to_string(), vec!["Idle".to_string()]);

        StateMachine {
            current_state: InfraState::Idle,
            allowed_transitions: transitions,
        }
    }

    fn get_state(&self) -> PyResult<String> {
        Ok(self.current_state.as_str().to_string())
    }

    fn transition(&mut self, next_state_str: &str) -> PyResult<String> {
        let current_str = self.current_state.as_str();
        
        if let Some(allowed) = self.allowed_transitions.get(current_str) {
            if allowed.contains(&next_state_str.to_string()) {
                if let Some(next_state) = InfraState::from_str(next_state_str) {
                    self.current_state = next_state;
                    return Ok(self.current_state.as_str().to_string());
                }
            }
        }
        
        Err(PyValueError::new_err(format!(
            "Invalid transition: {} -> {}", 
            current_str, next_state_str
        )))
    }
}

#[pymodule]
fn supervisor_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<StateMachine>()?;
    Ok(())
}
