import React from 'react';
import { Form, Input, Button, DatePicker, Select, message } from 'antd';
import moment from 'moment';
import axios from 'axios';

const ExhibitionForm = ({ initialValues, onSubmit }) => {
    const [form] = Form.useForm();
    const [employees, setEmployees] = React.useState([]);

    React.useEffect(() => {
        // Функция для получения данных сотрудников с бэкенда
        const fetchEmployees = async () => {
            try {
                const response = await axios.get('http://localhost:5000/employee_list');
                setEmployees(response.data);
            } catch (error) {
                console.error('Ошибка при получении сотрудников:', error);
                message.error('Не удалось загрузить сотрудников. Пожалуйста, попробуйте позже.');
            }
        };

        fetchEmployees();
    }, []);

    React.useEffect(() => {
        if (initialValues) {
            form.setFieldsValue({
                ...initialValues,
                start_date: initialValues.start_date ? moment(initialValues.start_date) : null,
                end_date: initialValues.end_date ? moment(initialValues.end_date) : null,
            });
        } else {
            form.resetFields();
        }
    }, [initialValues, form]);

    const handleFinish = (values) => {
        onSubmit({
            ...values,
            start_date: values.start_date.format('YYYY-MM-DD'),
            end_date: values.end_date ? values.end_date.format('YYYY-MM-DD') : null,
        });
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
                name="title" 
                label="Название" 
                rules={[{ required: true, message: 'Пожалуйста, введите название' }]}
            >
                <Input />
            </Form.Item>
            <Form.Item 
                name="description" 
                label="Описание" 
                rules={[{ required: true, message: 'Пожалуйста, введите описание' }]}
            >
                <Input />
            </Form.Item>
            <Form.Item 
                name="start_date" 
                label="Дата начала" 
                rules={[{ required: true, message: 'Пожалуйста, выберите дату начала' }]}
            >
                <DatePicker />
            </Form.Item>
            <Form.Item 
                name="end_date" 
                label="Дата конца"
            >
                <DatePicker />
            </Form.Item>
            <Form.Item 
                name="working_schedule" 
                label="Расписание" 
                rules={[{ required: true, message: 'Пожалуйста, введите расписание' }]}
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

export default ExhibitionForm;
