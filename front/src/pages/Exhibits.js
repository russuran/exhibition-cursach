import React, { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, Row, Col } from 'antd';
import axios from 'axios';
import ExhibitForm from '../components/ExhibitForm';

const Exhibits = () => {
    const [exhibits, setExhibits] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [currentExhibit, setCurrentExhibit] = useState(null);
    const [filters, setFilters] = useState({
        title: '',
        author: '',
        year_created: '',
        country_of_origin: '',
        material: ''
    });

    useEffect(() => {
        fetchExhibits();
    }, []);

    const fetchExhibits = async () => {
        const response = await axios.get('http://localhost:5000/exhibits/');
        setExhibits(response.data);
    };

    const handleDelete = async (exhibitId) => {
        await axios.delete(`http://localhost:5000/exhibits/${exhibitId}`);
        fetchExhibits();
    };

    const handleModalOpen = (exhibit) => {
        setCurrentExhibit(exhibit);
        setIsModalVisible(true);
    };

    const handleModalClose = () => {
        setCurrentExhibit(null);
        setIsModalVisible(false);
    };

    const handleFormSubmit = async (values) => {
        if (currentExhibit) {
            await axios.put(`http://localhost:5000/exhibits/${currentExhibit.exhibit_id}`, values);
        } else {
            await axios.post('http://localhost:5000/exhibits/', values);
        }
        fetchExhibits();
        handleModalClose();
    };

    const handleFilterChange = (e) => {
        const { name, value } = e.target;
        setFilters({
            ...filters,
            [name]: value
        });
    };


    const filteredExhibits = exhibits.filter(exhibit => {
        return (
            exhibit.title.toLowerCase().includes(filters.title.toLowerCase()) &&
            exhibit.author.toLowerCase().includes(filters.author.toLowerCase()) &&
            (filters.year_created ? exhibit.year_created === parseInt(filters.year_created) : true) &&
            exhibit.country_of_origin.toLowerCase().includes(filters.country_of_origin.toLowerCase()) &&
            exhibit.material.toLowerCase().includes(filters.material.toLowerCase())
        );
    });

    return (
        <div>
            <Row gutter={16} style={{ marginBottom: 16 }}>
                <Col span={5}>
                    <Input
                        placeholder="Название"
                        name="title"
                        value={filters.title}
                        onChange={handleFilterChange}
                    />
                </Col>
                <Col span={5}>
                    <Input
                        placeholder="Автор"
                        name="author"
                        value={filters.author}
                        onChange={handleFilterChange}
                    />
                </Col>
                <Col span={5}>
                    <Input
                        placeholder="Год создания"
                        name="year_created"
                        value={filters.year_created}
                        onChange={handleFilterChange}
                    />
                </Col>
                <Col span={5}>
                    <Input
                        placeholder="Страна происхождения"
                        name="country_of_origin"
                        value={filters.country_of_origin}
                        onChange={handleFilterChange}
                    />
                </Col>
                <Col span={4}>
                    <Input
                        placeholder="Материал"
                        name="material"
                        value={filters.material}
                        onChange={handleFilterChange}
                    />
                </Col>
            </Row>
            <Button type="primary" onClick={() => handleModalOpen(null)} style={{ marginBottom: 16 }}>
                Добавить экспонат
            </Button>
            <Table dataSource={filteredExhibits} rowKey="exhibit_id">
                <Table.Column title="Название" dataIndex="title" />
                <Table.Column title="Описание" dataIndex="description" />
                <Table.Column title="Автор" dataIndex="author" />
                <Table.Column title="Год создания" dataIndex="year_created" />
                <Table.Column title="Страна происхождения" dataIndex="country_of_origin" />
                <Table.Column title="Материал" dataIndex="material" />
                <Table.Column title="Действия" render={(text, exhibit) => (
                    <div style={{ display: 'flex', gap: '10px' }}>
                                                <Button onClick={() => handleModalOpen(exhibit)}>Редактировать</Button>
                        <Button onClick={() => handleDelete(exhibit.exhibit_id)}>Удалить</Button>
                    </div>
                )} />
            </Table>
            <Modal
                title={currentExhibit ? "Редактировать экспонат" : "Добавить экспонат"}
                visible={isModalVisible}
                onCancel={handleModalClose}
                footer={null}
            >
                <ExhibitForm
                    initialValues={currentExhibit}
                    onSubmit={handleFormSubmit}
                />
            </Modal>
        </div>
    );
};

export default Exhibits;

