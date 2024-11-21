import React from 'react';
import { Form, Input, Button, Select, message } from 'antd';
import axios from 'axios';

const RestorationForm = ({ initialValues, onSubmit }) => {
    const [form] = Form.useForm();
    const [exhibits, setExhibits] = React.useState([]);
    const [employees, setEmployees] = React.useState([]);

    React.useEffect(() => {
        // Fetch exhibits
        const fetchExhibits = async () => {
            try {
                const response = await axios.get('http://localhost:5000/exhibit_list');
                setExhibits(response.data);
            } catch (error) {
                console.error('Ошибка при получении экспонатов:', error);
                message.error('Не удалось загрузить экспонаты. Пожалуйста, попробуйте позже.');
            }
        };

        // Fetch employees
        const fetchEmployees = async () => {
            try {
                const response = await axios.get('http://localhost:5000/employee_list');
                setEmployees(response.data);
            } catch (error) {
                console.error('Ошибка при получении сотрудников:', error);
                message.error('Не удалось загрузить сотрудников. Пожалуйста, попробуйте позже.');
            }
        };

        fetchExhibits();
        fetchEmployees();
    }, []);

    React.useEffect(() => {
        if (initialValues) {
            form.setFieldsValue(initialValues);
        } else {
            form.resetFields();
        }
    }, [initialValues, form]);

    const handleFinish = (values) => {
        onSubmit(values);
    };

    return (
        <Form 
            form={form} 
            onFinish={handleFinish} 
            labelCol={{ span: 10 }} 
            layout="vertical" 
            style={{ maxWidth: 600 }}
        >
            <Form.Item 
                name="exhibit_id" 
                label="Экспонат" 
                rules={[{ required: true, message: 'Пожалуйста, выберите экспонат' }]}
            >
                <Select placeholder="Выберите экспонат">
                    {exhibits.map(exhibit => (
                        <Select.Option key={exhibit.id} value={exhibit.id}>
                            {exhibit.name} {/* Assuming exhibit has a name property */}
                        </Select.Option>
                    ))}
                </Select>
            </Form.Item>
            <Form.Item 
                name="employee_id" 
                label="Сотрудник" 
                rules={[{ required: true, message: 'Пожалуйста, выберите сотрудника' }]}
            >
                <Select placeholder="Выберите сотрудника">
                    {employees.map(employee => (
                        <Select.Option key={employee.id} value={employee.id}>
                            {employee.name} {/* Assuming employee has a name property */}
                        </Select.Option>
                    ))}
                </Select>
            </Form.Item>
            <Form.Item 
                name="start_date" 
                label="Дата начала" 
                rules={[{ required: true, message: 'Пожалуйста, выберите дату начала' }]}
            >
                <Input type="date" />
            </Form.Item>
            <Form.Item 
                name="end_date" 
                label="Дата конца"
            >
                <Input type="date" />
            </Form.Item>
            <Form.Item 
                name="restoration_reason" 
                label="Причина реставрации" 
                rules={[{ required: true, message: 'Пожалуйста, введите причину реставрации' }]}
            >
                <Input />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Сохранить
                </Button>
            </Form.Item>
        </Form>
    );
};

export default RestorationForm;
