import React, { useState } from "react";
import './HealthRecordForm.css';
import api from '../services/api';

const HealthRecordForm = ({ onRecordAdded, onCancel }) => {
    const [formData, setFormData] = useState({
        measurement_type: '',
        value: '',
        unit: '',
        notes: '',
        measured_at: new Date().toISOString().slice(0, 16)
    });
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const measurementTypes = {
        'weight': { label: 'Weight', unit: 'kg', min: 30, max: 300 },
        'height': { label: 'Height', unit: 'cm', min: 100, max: 250 },
        'blood_pressure_systolic': { label: 'Blood Pressure (Systolic)', unit: 'mmHg', min: 80, max: 200 },
        'blood_pressure_diastolic': { label: 'Blood Pressure (Diastolic)', unit: 'mmHg', min: 40, max: 120 },
        'heart_rate': { label: 'Heart Rate', unit: 'bpm', min: 40, max: 200 },
        'blood_glucose': { label: 'Blood Glucose', unit: 'mg/dL', min: 50, max: 400 },
        'temperature': { label: 'Body Temperature', unit: '°C', min: 35, max: 42 },
        'steps': { label: 'Steps', unit: 'steps', min: 0, max: 50000 },
        'sleep_duration': { label: 'Sleep Duration', unit: 'hours', min: 0, max: 24 }
    }

    const handleMeasurementTypeChange = (e) => {
        const selectedType = e.target.value;
        const typeConfig = measurementTypes[selectedType]
    
        setFormData(prev => ({
            ...prev,
            measurement_type: selectedType,
            unit: typeConfig?.unit || '',
            value: ''
        }));

        setErrors(prev => ({
            ...prev,
            measurement_type: '',
            value: ''
        }));
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));

        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const validateForm = () => {
        const newErrors = {};

        // Required fields
        if (!formData.measurement_type) {
            newErrors.measurement_type = 'Please select a measurement type';
        }

        if (!formData.value) {
            newErrors.value = 'Please enter a value';
        } else {
            const numValue = parseFloat(formData.value);
            if (isNaN(numValue)) {
                newErrors.value = 'Please enter a valid number';
            } else {
                const typeConfig = measurementTypes[formData.measurement_type];
                if (typeConfig && (numValue < typeConfig.min || numValue > typeConfig.max)) {
                    newErrors.value = `Value must be between ${typeConfig.min} and ${typeConfig.max} ${typeConfig.unit}`;
                }
            }
        }
    
        if (!formData.measured_at) {
            newErrors.measured_at = 'Please select date and time';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!validateForm()) {
            return;
        }

        setLoading(true);
        
        try {
            // Prepare data for API
            const recordData = {
                measurement_type: formData.measurement_type,
                value: parseFloat(formData.value),
                unit: formData.unit,
                notes: formData.notes || null,
                measured_at: new Date(formData.measured_at).toISOString()
            };

            //  API call
            const result = await api.addHealthRecord(recordData);
            alert('Health record added succesfully!');
            
            // Notify parent component first to trigger refresh
            if (onRecordAdded) {
                onRecordAdded(recordData);
            }
            
            // Reset form after successful submission
            setFormData({
                measurement_type: '',
                value: '',
                unit: '',
                notes: '',
                measured_at: new Date().toISOString().slice(0, 16)
            });

        } catch (error) {
            console.error('Error adding health record:', error);
            alert('Failed to add health record. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const selectedTypeConfig = measurementTypes[formData.measurement_type];

    return (
        <div className="health-record-form-container">
        <div className="health-record-form-card">
            <div className="form-header">
            <h2>Add Health Record</h2>
            <p>Track your health measurements</p>
            </div>

        <form onSubmit={handleSubmit} className="health-record-form">
          {/* Measurement Type Selection */}
          <div className="form-group">
            <label htmlFor="measurement_type">
              Measurement Type <span className="required">*</span>
            </label>
            <select
              id="measurement_type"
              name="measurement_type"
              value={formData.measurement_type}
              onChange={handleMeasurementTypeChange}
              className={errors.measurement_type ? 'error' : ''}
              disabled={loading}
            >
              <option value="">Select measurement type</option>
              {Object.entries(measurementTypes).map(([key, config]) => (
                <option key={key} value={key}>
                  {config.label}
                </option>
              ))}
            </select>
            {errors.measurement_type && (
              <span className="error-text">{errors.measurement_type}</span>
            )}
          </div>

          {/* Value Input */}
          <div className="form-group">
            <label htmlFor="value">
              Value <span className="required">*</span>
              {selectedTypeConfig && (
                <span className="hint">
                  ({selectedTypeConfig.min} - {selectedTypeConfig.max} {selectedTypeConfig.unit})
                </span>
              )}
            </label>
            <div className="value-input-group">
              <input
                type="number"
                id="value"
                name="value"
                value={formData.value}
                onChange={handleInputChange}
                placeholder={selectedTypeConfig ? `Enter value (${selectedTypeConfig.unit})` : 'Enter value'}
                step="0.1"
                min={selectedTypeConfig?.min}
                max={selectedTypeConfig?.max}
                className={errors.value ? 'error' : ''}
                disabled={loading || !formData.measurement_type}
              />
              {formData.unit && (
                <span className="unit-display">{formData.unit}</span>
              )}
            </div>
            {errors.value && (
              <span className="error-text">{errors.value}</span>
            )}
          </div>

          {/* Date and Time */}
          <div className="form-group">
            <label htmlFor="measured_at">
              Date & Time <span className="required">*</span>
            </label>
            <input
              type="datetime-local"
              id="measured_at"
              name="measured_at"
              value={formData.measured_at}
              onChange={handleInputChange}
              max={new Date().toISOString().slice(0, 16)}
              className={errors.measured_at ? 'error' : ''}
              disabled={loading}
            />
            {errors.measured_at && (
              <span className="error-text">{errors.measured_at}</span>
            )}
          </div>

          {/* Notes */}
          <div className="form-group">
            <label htmlFor="notes">Notes (Optional)</label>
            <textarea
              id="notes"
              name="notes"
              value={formData.notes}
              onChange={handleInputChange}
              placeholder="Add any additional notes about this measurement..."
              rows="3"
              disabled={loading}
            />
          </div>

          {/* Form Actions */}
          <div className="form-actions">
            {onCancel && (
              <button
                type="button"
                onClick={onCancel}
                className="btn-secondary"
                disabled={loading}
              >
                Cancel
              </button>
            )}
            <button
              type="submit"
              className="btn-primary"
              disabled={loading || !formData.measurement_type || !formData.value}
            >
              {loading ? 'Adding...' : 'Add Record'}
            </button>
          </div>
        </form>
      </div>
    </div>
    )
}

export default HealthRecordForm;